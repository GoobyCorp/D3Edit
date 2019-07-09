import db
import json
import random
import tkinter as tk
from pb2_resources import Items_pb2


def gbid_get(gbid):
    try:
        gbid_return = db.get_item_from_gbid(gbid)[0]
    except IndexError:
        gbid_return = 'Unknown Item ID: {}'.format(gbid)
        query = "insert or ignore into unknown(id, type) values({0}, 'item')".format(gbid)
        db.instance_and_run(query)
    return gbid_return


def affix_to_str(affix):
    try:
        affix_return = db.get_affix_from_id(affix)[0][3]
    except IndexError:
        affix_return = 'Unknown Affix {}'.format(affix)
        query = "insert or ignore into unknown(id, type) values({0}, 'affix')".format(affix)
        db.instance_and_run(query)
    return affix_return

def affix_checked(affix):
    try:
        affix_is_checked = db.get_affix_from_id(affix)[0][5]
    except IndexError:
        affix_is_checked = "Not Sure"
    return affix_is_checked

def decode_single_item(item):
    enchanted = False
    decoded_item = {}
    gbid = str(item.generator.gb_handle.gbid)
    decoded_gbid = gbid_get(gbid)
    if isinstance(decoded_gbid, tuple):
        decoded_item['name'] = "{0} ID: {1}".format(decoded_gbid[1], gbid)
        decoded_item['category'] = decoded_gbid[2]
        decoded_item['stackable'] = decoded_gbid[3]
        if decoded_item['stackable'] == 'True':
            decoded_item['stackable'] = True
        else:
            decoded_item['stackable'] = False
        legal_affix_list = db.get_legal_affixes(decoded_item['category'])
        decoded_item['legal_affixes'] = []
        if legal_affix_list:
            for line in legal_affix_list:
                if line[0]:
                    add = json.loads(line[0].replace("'", ''))
                    decoded_item['legal_affixes'].extend(add)
    else:
        decoded_item['name'] = decoded_gbid
        decoded_item['category'] = 'Unknown Category'
        decoded_item['stackable'] = False
    decoded_item['affixes'] = []

    try:
        enchanted = (int(item.generator.enchanted_affix_old), int(item.generator.enchanted_affix_new))
        if enchanted[0] == -1:
            enchanted = False
    except AttributeError:
        pass

    for affix in item.generator.base_affixes:
        desc = tk.StringVar(value=affix_to_str(affix))
        checked = affix_checked(affix)
        decoded_item['affixes'].append((affix, desc, checked))

    decoded_item['item'] = item
    decoded_item['jewel_rank'] = tk.StringVar(value=item.generator.jewel_rank)
    decoded_item['slot'] = db.get_slot(int(item.item_slot))[0][1]
    decoded_item['stack_size'] = tk.StringVar(value=item.generator.stack_size)
    if enchanted:
        decoded_item['enchanted'] = []
        decoded_item['enchanted'].append(enchanted)
        decoded_item['enchanted'].append(tk.StringVar(value=affix_to_str(enchanted[1])))
        decoded_item['enchanted'].append(affix_checked(enchanted[1]))

    decoded_item['primal'] = item.generator.flags == 59657
    decoded_item['ancient'] = item.generator.flags == 44297
    return decoded_item



def decode_itemlist(itemlist):
    item_out = []
    for item in itemlist:
        item_out.append(decode_single_item(item))
    return item_out


def gen_seed():
    seed = random.randint(3000000, 2147483646)
    return seed


def reroll_item(item):
    seed = gen_seed()
    item.generator.seed = seed
    return item

def set_flag(item):
    item.generator.flags = 59657
    return item

def generate_item(ids, affixnum):
    ids = int(ids)
    affixnum = int(affixnum)
    seed = gen_seed()
    idlow = random.randint(2014000000, 2029999999)
    item = Items_pb2.SavedItem()
    item.hireling_class = 0
    item.used_socket_count = 0
    item.id.id_high = 1
    item.id.id_low = idlow
    item.generator.seed = seed
    item.generator.gb_handle.game_balance_type = 2
    item.generator.gb_handle.gbid = ids
    item.generator.flags = 43273
    item.generator.item_binding_level = 2
    item.generator.stack_size = 1
    item.generator.season_created = 0
    item.generator.durability = 444
    for i in range(0, affixnum):
        item.generator.base_affixes.append(0)
    return item
