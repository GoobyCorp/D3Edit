#!/usr/bin/env python3

from json import load
from sys import getsizeof
from struct import pack, unpack
from argparse import ArgumentParser
from os.path import isfile, isdir, join
from binascii import hexlify as _hexlify

# pip3 install protobuf
import Account_pb2

BYTE_MAX_VALUE = 255
XOR_KEY = 0x305F92D82EC9A01B

GBIDS_FILE = "gbids.json"
SLOTS_FILE = "slots.json"
AFFIXES_FILE = "affixes.json"
CURRENCY_FILE = "currencies.json"

HERO_DIR = "heroes"
ASSET_DIR = "assets"

def hexlify(b: (bytes, bytearray)) -> (bytes, bytearray):
    """
    bytes -> hex
    :param b: the bytes you want to convert to hex
    :return: the hex string representation of the specified bytes
    """
    return _hexlify(b).decode("utf8")

def truncate(num: int, boundary: int, signed: bool, endian: str = "little") -> int:
    """
    Truncate an int to a given byte boundary
    :param num: the number to truncate
    :param margin: the byte boundary
    :param signed: whether or not the int is signed
    :param endian: the integer's endianness
    :return: the truncated integer
    """
    return int.from_bytes(num.to_bytes(getsizeof(num), endian, signed=signed)[:boundary], endian, signed=signed)

def decrypt_save(data: (bytes, bytearray)) -> (bytes, bytearray):
    """
    Decrypt a save file
    :param data: the save data to decrypt
    :return: the decrypted save data
    """
    global XOR_KEY

    if isinstance(data, bytes):
        data = bytearray(data)

    num = XOR_KEY
    for i in range(len(data)):
        data[i] ^= (num & BYTE_MAX_VALUE)
        num = truncate((((num ^ data[i]) << 56) | num >> 8), 8, False)

    return bytes(data)

def encrypt_save(data: (bytes, bytearray)) -> (bytes, bytearray):
    """
    Encrypt a save file
    :param data: the save data to encrypt
    :return: the encrypted save data
    """
    global XOR_KEY

    if isinstance(data, bytes):
        data = bytearray(data)

    num1 = XOR_KEY
    for i in range(len(data)):
        num2 = data[i]
        data[i] ^= (num1 & BYTE_MAX_VALUE)
        num1 = truncate(((num1 ^ num2) << 56) | num1 >> 8, 8, False)

    return bytes(data)

if __name__ == "__main__":
    # parse arguments
    parser = ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-i", "--in-file", type=str, required=True, help="The account file you want to work with")
    parser.add_argument("-o", "--out-file", type=str, help="The account file you want to output to")
    mod_group = parser.add_argument_group("modifications")
    mod_group.add_argument("--gold", type=int, help="The amount of gold you want your characters to have")
    mod_group.add_argument("--blood-shards", type=int, help="The amount of blood shards you want your characters to have")
    mod_group.add_argument("--reusable-parts", type=int, help="The amount of reusable parts you want your characters to have")
    mod_group.add_argument("--arcane-dust", type=int, help="The amount of arcane dust you want your characters to have")
    mod_group.add_argument("--veiled-crystals", type=int, help="The amount of veiled crystals you want your characters to have")
    mod_group.add_argument("--deaths-breath", type=int, help="The amount of deaths breath you want your characters to have")
    mod_group.add_argument("--forgotten-souls", type=int, help="The amount of forgotten souls you want your characters to have")
    mod_group.add_argument("--khanduran-runes", type=int, help="The amount of Khanduran runes you want your characters to have")
    mod_group.add_argument("--caldeum-nightshade", type=int, help="The amount of Caldeum nightshade you want your characters to have")
    mod_group.add_argument("--arreat-war-tapestries", type=int, help="The amount of Arret War tapestries you want your characters to have")
    mod_group.add_argument("--corrupted-angel-flesh", type=int, help="The amount of corrupted angel flesh you want your characters to have")
    mod_group.add_argument("--westmarch-holy-water", type=int, help="The amount of Westmarch holy water you want your characters to have")
    mod_group.add_argument("--hearts-of-fright", type=int, help="The amount of hearts of fright you want your characters to have")
    mod_group.add_argument("--vials-of-putridness", type=int, help="The amount of vials of putridness you want your characters to have")
    mod_group.add_argument("--idols-of-terror", type=int, help="The amount of idols of terror you want your characters to have")
    mod_group.add_argument("--leorics-regrets", type=int, help="The amount of Leoric's regrets you want your characters to have")
    mod_group.add_argument("--vengeful-eyes", type=int, help="The amount of vengeful eyes you want your characters to have")
    mod_group.add_argument("--writhing-spines", type=int, help="The amount of writhing spines you want your characters to have")
    mod_group.add_argument("--devils-fangs", type=int, help="The amount of devil's fangs you want your characters to have")
    mod_group.add_argument("--all-currencies", type=int, help="Set all currencies to the given value")
    args = parser.parse_args()

    # make sure the input file exists
    assert isfile(args.in_file), "input file doesn't exist"

    # make sure assets exist
    assert isfile(join(ASSET_DIR, GBIDS_FILE)), "%s doesn't exist" % (GBIDS_FILE)
    assert isfile(join(ASSET_DIR, AFFIXES_FILE)), "%s doesn't exist" % (AFFIXES_FILE)
    assert isfile(join(ASSET_DIR, CURRENCY_FILE)), "%s doesn't exist" % (CURRENCY_FILE)

    # load assets
    with open(join(ASSET_DIR, GBIDS_FILE), "r") as f:
        gbid_list = load(f)
    with open(join(ASSET_DIR, AFFIXES_FILE), "r") as f:
        affix_list = load(f)
    with open(join(ASSET_DIR, CURRENCY_FILE), "r") as f:
        currency_list = load(f)
    with open(join(ASSET_DIR, SLOTS_FILE), "r") as f:
        slot_list = load(f)

    # account
    # decrypt
    with open(args.in_file, "rb") as f:
        account_enc = f.read()
    account_dec = decrypt_save(account_enc)

    # parse
    asd = Account_pb2.SavedDefinition()
    asd.ParseFromString(account_dec)

    # I hope you can handle super redundant logic (because I can't)
    # modify account here
    for i in range(len(asd.partitions)):
        if len(asd.partitions[i].currency_data.currency) > 0:
            # gold
            if args.gold or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 1:
                    if args.gold:
                        asd.partitions[i].currency_data.currency[0].count = args.gold
                        print("Set slot %s gold to %s" % (i, args.gold))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[0].count = args.all_currencies
                        print("Set slot %s gold to %s" % (i, args.all_currencies))
            # blood shards
            if args.blood_shards or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 2:
                    if args.blood_shards:
                        asd.partitions[i].currency_data.currency[1].count = args.blood_shards
                        print("Set slot %s blood shards to %s" % (i, args.blood_shards))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[1].count = args.all_currencies
                        print("Set slot %s blood shards to %s" % (i, args.all_currencies))
            # reusable parts
            if args.reusable_parts or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 3:
                    if args.reusable_parts:
                        asd.partitions[i].currency_data.currency[2].count = args.reusable_parts
                        print("Set slot %s reusable parts to %s" % (i, args.reusable_parts))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[2].count = args.all_currencies
                        print("Set slot %s reusable parts to %s" % (i, args.all_currencies))
            # arcane dust
            if args.arcane_dust or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 4:
                    if args.arcane_dust:
                        asd.partitions[i].currency_data.currency[3].count = args.arcane_dust
                        print("Set slot %s arcane dust to %s" % (i, args.arcane_dust))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[3].count = args.all_currencies
                        print("Set slot %s arcane dust to %s" % (i, args.all_currencies))
            # veiled crystals
            if args.veiled_crystals or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 5:
                    if args.veiled_crystals:
                        asd.partitions[i].currency_data.currency[4].count = args.veiled_crystals
                        print("Set slot %s veiled crystals to %s" % (i, args.veiled_crystals))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[4].count = args.all_currencies
                        print("Set slot %s veiled crystals to %s" % (i, args.all_currencies))
            # deaths breath
            if args.deaths_breath or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 6:
                    if args.deaths_breath:
                        asd.partitions[i].currency_data.currency[5].count = args.deaths_breath
                        print("Set slot %s deaths breath to %s" % (i, args.deaths_breath))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[5].count = args.all_currencies
                        print("Set slot %s deaths breath to %s" % (i, args.all_currencies))
            # forgotten souls
            if args.forgotten_souls or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 7:
                    if args.forgotten_souls:
                        asd.partitions[i].currency_data.currency[6].count = args.forgotten_souls
                        print("Set slot %s forgotten souls to %s" % (i, args.forgotten_souls))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[6].count = args.all_currencies
                        print("Set slot %s forgotten souls to %s" % (i, args.all_currencies))
            # khanduran runes
            if args.khanduran_runes or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 8:
                    if args.khanduran_runes:
                        asd.partitions[i].currency_data.currency[7].count = args.khanduran_runes
                        print("Set slot %s Khanduran runes to %s" % (i, args.khanduran_runes))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[7].count = args.all_currencies
                        print("Set slot %s Khanduran runes to %s" % (i, args.all_currencies))
            # caldeum nightshade
            if args.caldeum_nightshade or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 9:
                    if args.caldeum_nightshade:
                        asd.partitions[i].currency_data.currency[8].count = args.caldeum_nightshade
                        print("Set slot %s Caldeum nightshade to %s" % (i, args.caldeum_nightshade))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[8].count = args.all_currencies
                        print("Set slot %s Caldeum nightshade to %s" % (i, args.all_currencies))
            # arreat war tapestries
            if args.arreat_war_tapestries or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 10:
                    if args.arreat_war_tapestries:
                        asd.partitions[i].currency_data.currency[9].count = args.arreat_war_tapestries
                        print("Set slot %s Arreat War tapestries to %s" % (i, args.arreat_war_tapestries))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[9].count = args.all_currencies
                        print("Set slot %s Arreat War tapestries to %s" % (i, args.all_currencies))
            # corrupted angel flesh
            if args.corrupted_angel_flesh or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 11:
                    if args.corrupted_angel_flesh:
                        asd.partitions[i].currency_data.currency[10].count = args.corrupted_angel_flesh
                        print("Set slot %s corrupted angel flesh to %s" % (i, args.corrupted_angel_flesh))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[10].count = args.all_currencies
                        print("Set slot %s corrupted angel flesh to %s" % (i, args.all_currencies))
            # westmarch holy water
            if args.westmarch_holy_water or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 12:
                    if args.westmarch_holy_water:
                        asd.partitions[i].currency_data.currency[11].count = args.westmarch_holy_water
                        print("Set slot %s Westmarch holy water to %s" % (i, args.westmarch_holy_water))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[11].count = args.all_currencies
                        print("Set slot %s Westmarch holy water to %s" % (i, args.all_currencies))
            # hearts of fright
            if args.hearts_of_fright or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 13:
                    if args.hearts_of_fright:
                        asd.partitions[i].currency_data.currency[12].count = args.hearts_of_fright
                        print("Set slot %s hearts of fright to %s" % (i, args.hearts_of_fright))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[12].count = args.all_currencies
                        print("Set slot %s hearts of fright to %s" % (i, args.all_currencies))
            # vials of putridness
            if args.vials_of_putridness or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 14:
                    if args.vials_of_putridness:
                        asd.partitions[i].currency_data.currency[13].count = args.vials_of_putridness
                        print("Set slot %s vials of putridness to %s" % (i, args.vials_of_putridness))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[13].count = args.all_currencies
                        print("Set slot %s vials of putridness to %s" % (i, args.all_currencies))
            # idols of terror
            if args.idols_of_terror or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 15:
                    if args.idols_of_terror:
                        asd.partitions[i].currency_data.currency[14].count = args.idols_of_terror
                        print("Set slot %s idols of terror to %s" % (i, args.idols_of_terror))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[14].count = args.all_currencies
                        print("Set slot %s idols of terror to %s" % (i, args.all_currencies))
            # leoric's regrets
            if args.leorics_regrets or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 16:
                    if args.leorics_regrets:
                        asd.partitions[i].currency_data.currency[15].count = args.leorics_regrets
                        print("Set slot %s Leoric's regrets to %s" % (i, args.leorics_regrets))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[15].count = args.all_currencies
                        print("Set slot %s Leoric's regrets to %s" % (i, args.all_currencies))
            # vengeful eyes
            if args.vengeful_eyes or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 17:
                    if args.vengeful_eyes:
                        asd.partitions[i].currency_data.currency[16].count = args.vengeful_eyes
                        print("Set slot %s vengeful eyes to %s" % (i, args.vengeful_eyes))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[16].count = args.all_currencies
                        print("Set slot %s vengeful eyes to %s" % (i, args.all_currencies))
            # writhing spines
            if args.writhing_spines or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 18:
                    if args.writhing_spines:
                        asd.partitions[i].currency_data.currency[17].count = args.writhing_spines
                        print("Set slot %s writhing spines to %s" % (i, args.writhing_spines))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[17].count = args.all_currencies
                        print("Set slot %s writhing spines to %s" % (i, args.all_currencies))
            # devil's fangs
            if args.devils_fangs or args.all_currencies:
                if len(asd.partitions[i].currency_data.currency) >= 19:
                    if args.devils_fangs:
                        asd.partitions[i].currency_data.currency[18].count = args.devils_fangs
                        print("Set slot %s devils's fangs to %s" % (i, args.devils_fangs))
                    elif args.all_currencies:
                        asd.partitions[i].currency_data.currency[18].count = args.all_currencies
                        print("Set slot %s devils's fangs to %s" % (i, args.all_currencies))

    # end account modifications
    account_mod_dec = asd.SerializeToString()
    account_mod_enc = encrypt_save(account_mod_dec)
    # output the modified account
    if args.out_file:
        with open(args.out_file, "wb") as f:
            f.write(account_mod_enc)
    # end account output