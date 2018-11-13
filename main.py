#!/usr/bin/env python3

from json import load
from sys import getsizeof
from struct import pack, unpack
from argparse import ArgumentParser
from os.path import isfile, isdir, join
from binascii import hexlify as _hexlify

# pip3 install protobuf
import Hero_pb2
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
    parser.add_argument("-i", "--in-file", type=str, required=True, help="The save file you want to work with")
    parser.add_argument("-o", "--out-file", type=str, help="The save file you want to output to")
    mod_group = parser.add_argument_group("modifications")
    mod_group.add_argument("--gold", type=int, help="The amount of gold you want your characters to have")
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
    if args.gold:
        for i in range(len(asd.partitions)):
            #for j in range(len(asd.partitions[i].currency_data.currency)):
            # asd.partitions[j].currency_data.currency[j].id
            if len(asd.partitions[i].currency_data.currency) > 0:
                asd.partitions[i].currency_data.currency[0].count = args.gold
                print("Set slot %s gold to %s" % (i, args.gold))
    # end account modifications
    account_mod_dec = asd.SerializeToString()
    account_mod_enc = encrypt_save(account_mod_dec)
    # output the modified account
    if args.out_file:
        with open(args.out_file, "wb") as f:
            f.write(account_mod_enc)
    # end account output

    # hero ID is in big endian for god knows why (maybe PS3 and Xbox 360 releases?)
    last_hero_save = hexlify(pack(">Q", asd.digest.last_played_hero_id.id_low))

    if isdir(join("saves", "Modded", HERO_DIR)):
        last_hero_save_path = join("saves", "Modded", HERO_DIR, last_hero_save + ".dat")
        if isfile(last_hero_save_path):
            with open(last_hero_save_path, "rb") as f:
                hero_enc = f.read()
            hero_dec = decrypt_save(hero_enc)
            hsd = Hero_pb2.SavedDefinition()
            hsd.ParseFromString(hero_dec)
            #print(hsd.items.items)
            for single in hsd.items.items:
                for affix in single.generator.base_affixes:
                    if str(affix) in affix_list:
                        print(affix_list[str(affix)])
                    else:
                        print("Unknown Affix: %s" % (affix))
            # modify hero here
            hero_mod_dec = hsd.SerializeToString()
            hero_mod_enc = encrypt_save(hero_mod_dec)
            # output the modified hero