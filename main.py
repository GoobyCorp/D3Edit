#!/usr/bin/env python3

from json import load
from os import linesep
from sys import getsizeof
from struct import pack, unpack
from argparse import ArgumentParser
from os.path import isfile, isdir, join
from binascii import hexlify as _hexlify

# pip3 install protobuf
import Hero_pb2
import Account_pb2

BYTE_MAX_VALUE = 255
XOR_KEY = 3485666093803610139

GBIDS_FILE = "gbids.json"
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

def parse_gbids(data: str) -> dict:
    ""
    gbids = {}
    for single in data.split(linesep):
        split_line = [x.strip() for x in single.split("=")]
        if len(split_line) == 4:
            if split_line[0] != "":
                split_line[0] = int(split_line[0])
            index = split_line.pop(0)
            gbids[index] = {"name": split_line[0], "category": split_line[1], "platform": split_line[2]}
    return gbids

def parse_affixes(data: str) -> dict:
    affixes = {}
    for single in data.split(linesep):
        split_line = [x.strip() for x in single.split("=")]
        if len(split_line) == 3:
            if split_line[0] != "":
                split_line[0] = int(split_line[0])
            index = split_line.pop(0)
            affixes[index] = {"effect": split_line[0], "effectiveness": split_line[1]}
    return affixes

if __name__ == "__main__":
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

    # account
    # decrypt
    with open(join("saves", "Modded", "account.dat"), "rb") as fr:
        account_enc = fr.read()
    account_dec = decrypt_save(account_enc)

    # parse
    asd = Account_pb2.SavedDefinition()
    asd.ParseFromString(account_dec)
    for partition in asd.partitions:
        currencies = partition.currency_data.currency
        for currency in currencies:
            if str(currency.id) in currency_list:
                print("%s: %s" % (currency_list[str(currency.id)], currency.count))
    # modify account here
    account_mod_dec = asd.SerializeToString()
    account_mod_enc = encrypt_save(account_mod_dec)

    # hero ID is in big endian for god knows why (maybe PS3 and Xbox 360 releases?)
    last_hero_save = hexlify(pack(">Q", asd.digest.last_played_hero_id.id_low))

    if isdir(join("saves", "Modded", HERO_DIR)):
        last_hero_save_path = join("saves", "Modded", HERO_DIR, last_hero_save + ".dat")
        if isfile(last_hero_save_path):
            with open(last_hero_save_path, "rb") as fr:
                hero_enc = fr.read()
            hero_dec = decrypt_save(hero_enc)
            hsd = Hero_pb2.SavedDefinition()
            hsd.ParseFromString(hero_dec)
            #print(hsd.items.items)
            for single in hsd.items.items:
                #print(single)
                gbid = single.generator.gb_handle.gbid
                if str(gbid) in gbid_list:
                    print(gbid_list[str(gbid)])
                else:
                    print("Unknown GBID: %s" % (gbid))
                for affix in single.generator.base_affixes:
                    if str(affix) in affix_list:
                        print(affix_list[str(affix)])
                    else:
                        print("Unknown Affix: %s" % (affix))
            # modify hero here
            hero_mod_dec = hsd.SerializeToString()
            hero_mod_enc = encrypt_save(hero_mod_dec)