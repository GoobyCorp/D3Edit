from pb2_resources import Hero_pb2, Account_pb2
import db
import glob
from os.path import dirname, basename
from save_manager import save_handler
from save_manager import item_handler
from struct import pack
import random


currency_list = {str(k): v for (k, v) in db.get_currency_list()}


class SaveData(object):
    def __init__(self, account_file, output_file=None):
        self.account_file = account_file
        self.save_folder = dirname(self.account_file)
        self.hero_files = glob.glob('{}/heroes/*.dat'.format(self.save_folder))
        self.output_file = output_file
        self.account_file = account_file
        # load encrypted save data
        self.account_enc = save_handler.load_encrypted_file(self.account_file)
        self.account_dec = save_handler.decrypt_save(self.account_enc)
        # load saved definition
        self.asd = Account_pb2.SavedDefinition()
        # parse decrypted save definitions
        self.asd.ParseFromString(self.account_dec)
        # load currency information
        self.currency_names = self.load_currencies()
        self.last_played_hero_id = save_handler.hexlify(pack(">Q", self.asd.digest.last_played_hero_id.id_low))
        # load last played hero
        self.heroes = {}
        self.hsd = Hero_pb2.SavedDefinition()
        for hero_path in self.hero_files:
            hero_id = basename(hero_path.replace('.dat', ''))
            self.heroes[hero_id] = Hero_pb2.SavedDefinition()
            enc_hero = save_handler.load_encrypted_file(hero_path)
            dec_hero = save_handler.decrypt_save(enc_hero)
            self.heroes[hero_id].ParseFromString(dec_hero)
            if isinstance(self.heroes[hero_id], int):
                del self.heroes[hero_id]

    def load_currencies(self):
        """
        Loads currencies from the account file.
        """
        currency_names = {}
        for partition in self.asd.partitions:
            currencies = partition.currency_data.currency
            for currency in currencies:
                currency_id = str(currency.id)
                if currency_id in currency_list:
                    currency_name = currency_list[currency_id]
                    currency_names[currency_name.lower().replace(' ', '-')] = currency_id
                    # print("Loaded %s: %s" % (currency_name, currency.count))
                else:
                    print("Unknown currency ID: %s" % currency.id)
        return currency_names

    def set_currency(self, currency_id, amount):
        """

        :param currency_id: int() id of the currency to modify
        :param amount: int() amount to set the currency to
        :return:
        """
        currency_id = int(currency_id)
        if str(currency_id) in list(self.currency_names.values()):
            for i in range(len(self.asd.partitions)):
                if len(self.asd.partitions[i].currency_data.currency) > 0:
                    current_currency = self.asd.partitions[i].currency_data.currency[currency_id]
                    current_currency.count = amount
                    print("Set currency {0} to {1}".format(
                        currency_list[str(currency_id)], current_currency.count, currency_id))
        else:
            print("Currency {0} not found on the account, this normally means you need to play and collect "
                  "some currency first.".format(currency_id))

    def set_attribute(self, partition: int, contents: tuple):
        attributes = self.asd.partitions[partition].saved_attributes.attributes
        keyfound = False
        for attribute in attributes:
            if attribute.key == contents[0]:
                keyfound = True
                attribute.value = contents[1]
        if not keyfound:
            added_attribute = attributes.add()
            added_attribute.key = contents[0]
            added_attribute.value = contents[1]

    def commit_account_changes(self, target_file=None):
        # TODO: perhaps automatically backup account.dat
        # serialize and encrypt account file
        if target_file:
            self.output_file = target_file
        account_mod_dec = self.asd.SerializeToString()
        account_mod_enc = save_handler.encrypt_save(account_mod_dec)
        # commit account file to storage only if it changed
        if self.output_file and (account_mod_enc != self.account_enc):
            save_handler.commit_to_file(account_mod_enc, self.output_file)

    def commit_hero_changes(self, hid):
        if hid.startswith('modded_'):
            target_file = "{0}/heroes/{1}.dat".format(self.save_folder, hid)
        else:
            target_file = "{0}/heroes/{1}.dat".format(self.save_folder, hid)
        hero_mod_dec = self.heroes[hid].SerializeToString()
        hero_mod_enc = save_handler.encrypt_save(hero_mod_dec)
        save_handler.commit_to_file(hero_mod_enc, target_file)
        return target_file

    def additem(self, affixnum=0, target_stash=None, ids=None, item=None, quality=None):
        assert target_stash, "Need a target stash to add the item to!"
        assert any([ids, item]), "Need either item or id to add"
        saved_attr = None
        if not item:
            newitem = item_handler.generate_item(ids, affixnum)
        else:
            newitem = item
            newitem.generator.seed = random.randint(3000000, 2147483646)
        if quality:
            newqual = db.get_quality_level(quality)
            newitem.generator.item_quality_level = int(newqual)
        account_stash = ['SC - Non Season', 'HC - Non Season', 'HC - Season', 'SC - Season']
        if target_stash == 'SC - Non Season':
            try:
                stash_data = self.asd.partitions[0].items.items
                saved_attr = self.asd.partitions[0].saved_attributes.attributes
            except IndexError:
                stash_data = None
        elif target_stash == 'HC - Non Season':
            try:
                stash_data = self.asd.partitions[1].items.items
                saved_attr = self.asd.partitions[1].saved_attributes.attributes
            except IndexError:
                stash_data = None
        elif target_stash == 'SC - Season':
            try:
                stash_data = self.asd.partitions[2].items.items
                saved_attr = self.asd.partitions[2].saved_attributes.attributes
            except IndexError:
                stash_data = None
        elif target_stash == 'HC - Season':
            try:
                stash_data = self.asd.partitions[3].items.items
                saved_attr = self.asd.partitions[3].saved_attributes.attributes
            except IndexError:
                stash_data = None
        else:
            hero_id = target_stash.split(' - ')[1]
            stash_data = self.heroes[hero_id].items.items
        assert stash_data, "Could not identify target stash!"
        if target_stash in account_stash:
            available_slots = [i for i in range(0, 20)]
            for attribute in saved_attr:
                if attribute.key == -4096:
                    available_slots = [i for i in range(0, attribute.value)]
            for i in stash_data:
                try:
                    available_slots.remove(i.square_index)
                except ValueError:
                    print("Item collition detected, two items in the same inventory slot!")
                    print("{0}, {1}".format(i.square_index, i.generator.seed))
            if available_slots:
                newitem.item_slot = 544
                it = stash_data.add()
                it.CopyFrom(newitem)
                it.square_index = available_slots[-1]
            else:
                print("Inventory is full!")
            self.commit_account_changes()
        else:
            available_slots = [i for i in range(0, 60)]
            for i in stash_data:
                if i.item_slot == 272:
                    try:
                        available_slots.remove(i.square_index)
                    except ValueError:
                        print("Item collition detected, two items in the same inventory slot!")
                        print("{0}, {1}".format(i.square_index, i.generator.seed))
            if available_slots:
                newitem.item_slot = 272
                it = stash_data.add()
                it.CopyFrom(newitem)
                it.square_index = available_slots[-1]
            self.commit_hero_changes(hero_id)
