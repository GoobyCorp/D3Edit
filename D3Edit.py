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
    mod_group.add_argument("--platinum", type=int, help="The amount of platinum you want your characters to have")
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
    mod_group.add_argument("--demon-organ-diablo", type=int, help="The amount of Diablo demon organs you want your characters to have")
    mod_group.add_argument("--demon-organ-ghom", type=int, help="The amount of Ghom demon organs you want your characters to have")
    mod_group.add_argument("--demon-organ-siege-breaker", type=int, help="The amount of siege breaker demon organs you want your characters to have")
    mod_group.add_argument("--demon-organ-skeleton-king", type=int, help="The amount of skeleton king demon organs you want your characters to have")
    mod_group.add_argument("--demon-organ-eyes", type=int, help="The amount of eye demon organs you want your characters to have")
    mod_group.add_argument("--demon-organ-spinal-cords", type=int, help="The amount of spinal cord demon organs you want your characters to have")
    mod_group.add_argument("--demon-organ-teeth", type=int, help="The amount of teeth demon organs you want your characters to have")
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
    for partition in asd.partitions:
        currencies = partition.currency_data.currency
        for currency in currencies:
            if str(currency.id) in currency_list:
                print("%s: %s" % (currency_list[str(currency.id)], currency.count))
            else:
                print("Unknown currency ID: %s" % (currency.id))
    # modify account here
    for i in range(len(asd.partitions)):
        #for j in range(len(asd.partitions[i].currency_data.currency)):
        # asd.partitions[j].currency_data.currency[j].id
        if len(asd.partitions[i].currency_data.currency) > 0:
            # gold
            if args.gold:
                if len(asd.partitions[i].currency_data.currency) >= 1:
                    asd.partitions[i].currency_data.currency[0].count = args.gold
                    print("Set slot %s gold to %s" % (i, args.gold))
            # blood shards
            if args.blood_shards:
                if len(asd.partitions[i].currency_data.currency) >= 2:
                    asd.partitions[i].currency_data.currency[1].count = args.blood_shards
                    print("Set slot %s blood shards to %s" % (i, args.blood_shards))
            # platinum
            if args.platinum:
                if len(asd.partitions[i].currency_data.currency) >= 3:
                    asd.partitions[i].currency_data.currency[2].count = args.platinum
                    print("Set slot %s platinum to %s" % (i, args.platinum))
            # reusable parts
            if args.reusable_parts:
                if len(asd.partitions[i].currency_data.currency) >= 4:
                    asd.partitions[i].currency_data.currency[3].count = args.reusable_parts
                    print("Set slot %s reusable parts to %s" % (i, args.reusable_parts))
            # arcane dust
            if args.arcane_dust:
                if len(asd.partitions[i].currency_data.currency) >= 5:
                    asd.partitions[i].currency_data.currency[4].count = args.arcane_dust
                    print("Set slot %s arcane dust to %s" % (i, args.arcane_dust))
            # veiled crystals
            if args.veiled_crystals:
                if len(asd.partitions[i].currency_data.currency) >= 6:
                    asd.partitions[i].currency_data.currency[5].count = args.veiled_crystals
                    print("Set slot %s veiled crystals to %s" % (i, args.veiled_crystals))
            # deaths breath
            if args.deaths_breath:
                if len(asd.partitions[i].currency_data.currency) >= 7:
                    asd.partitions[i].currency_data.currency[6].count = args.deaths_breath
                    print("Set slot %s deaths breath to %s" % (i, args.deaths_breath))
            # forgotten souls
            if args.forgotten_souls:
                if len(asd.partitions[i].currency_data.currency) >= 8:
                    asd.partitions[i].currency_data.currency[7].count = args.forgotten_souls
                    print("Set slot %s forgotten souls to %s" % (i, args.forgotten_souls))
            # khanduran runes
            if args.khanduran_runes:
                if len(asd.partitions[i].currency_data.currency) >= 9:
                    asd.partitions[i].currency_data.currency[8].count = args.khanduran_runes
                    print("Set slot %s Khanduran runes to %s" % (i, args.khanduran_runes))
            # caldeum nightshade
            if args.caldeum_nightshade:
                if len(asd.partitions[i].currency_data.currency) >= 10:
                    asd.partitions[i].currency_data.currency[9].count = args.caldeum_nightshade
                    print("Set slot %s Caldeum nightshade to %s" % (i, args.caldeum_nightshade))
            # arreat war tapestries
            if args.arreat_war_tapestries:
                if len(asd.partitions[i].currency_data.currency) >= 11:
                    asd.partitions[i].currency_data.currency[10].count = args.veiled_crystals
                    print("Set slot %s Arreat War tapestries to %s" % (i, args.veiled_crystals))
            # corrupted angel flesh
            if args.corrupted_angel_flesh:
                if len(asd.partitions[i].currency_data.currency) >= 12:
                    asd.partitions[i].currency_data.currency[11].count = args.corrupted_angel_flesh
                    print("Set slot %s corrupted angel flesh to %s" % (i, args.corrupted_angel_flesh))
            # westmarch holy water
            if args.westmarch_holy_water:
                if len(asd.partitions[i].currency_data.currency) >= 13:
                    asd.partitions[i].currency_data.currency[12].count = args.westmarch_holy_water
                    print("Set slot %s Westmarch holy water to %s" % (i, args.westmarch_holy_water))
            # demon organ - diablo
            if args.demon_organ_diablo:
                if len(asd.partitions[i].currency_data.currency) >= 14:
                    asd.partitions[i].currency_data.currency[13].count = args.demon_organ_diablo
                    print("Set slot %s Diablo demon organs to %s" % (i, args.demon_organ_diablo))
            # demon organ - ghom
            if args.demon_organ_ghom:
                if len(asd.partitions[i].currency_data.currency) >= 15:
                    asd.partitions[i].currency_data.currency[14].count = args.demon_organ_ghom
                    print("Set slot %s Ghom demon organs to %s" % (i, args.demon_organ_ghom))
            # demon organ - siege breaker
            if args.demon_organ_siege_breaker:
                if len(asd.partitions[i].currency_data.currency) >= 16:
                    asd.partitions[i].currency_data.currency[15].count = args.demon_organ_siege_breaker
                    print("Set slot %s siege breaker demon organs to %s" % (i, args.demon_organ_siege_breaker))
            # demon organ - skeleton king
            if args.demon_organ_skeleton_king:
                if len(asd.partitions[i].currency_data.currency) >= 17:
                    asd.partitions[i].currency_data.currency[16].count = args.demon_organ_skeleton_king
                    print("Set slot %s skeleton king demon organs to %s" % (i, args.demon_organ_skeleton_king))
            # demon organ - eye
            if args.demon_organ_eyes:
                if len(asd.partitions[i].currency_data.currency) >= 18:
                    asd.partitions[i].currency_data.currency[17].count = args.demon_organ_eyes
                    print("Set slot %s eye demon organs to %s" % (i, args.demon_organ_eyes))
            # demon organ - spinal cord
            if args.demon_organ_spinal_cords:
                if len(asd.partitions[i].currency_data.currency) >= 19:
                    asd.partitions[i].currency_data.currency[18].count = args.demon_organ_spinal_cords
                    print("Set slot %s spinal cord demon organs to %s" % (i, args.demon_organ_spinal_cords))
            # demon organ - teeth
            if args.demon_organ_teeth:
                if len(asd.partitions[i].currency_data.currency) >= 20:
                    asd.partitions[i].currency_data.currency[19].count = args.demon_organ_teeth
                    print("Set slot %s teeth demon organs to %s" % (i, args.demon_organ_teeth))

    # end account modifications
    account_mod_dec = asd.SerializeToString()
    account_mod_enc = encrypt_save(account_mod_dec)
    # output the modified account
    if args.out_file:
        with open(args.out_file, "wb") as f:
            f.write(account_mod_enc)
    # end account output