#!/usr/bin/env python3

from json import load
from sys import getsizeof
from os.path import isfile, join
from argparse import ArgumentParser
from binascii import hexlify as _hexlify

# pip3 install protobuf
import Account_pb2

BYTE_MAX_VALUE = 255
XOR_KEY = 0x305F92D82EC9A01B

SETTINGS_FILE = "settings.json"

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
    # make sure settings exist
    assert isfile(SETTINGS_FILE), "%s doesn't exist" % (SETTINGS_FILE)

    # load settings
    with open(SETTINGS_FILE, "r") as f:
        settings = load(f)

    # make sure assets exist
    assert isfile(join(settings["asset_dir"], settings["gbids_file"])), "%s doesn't exist" % (settings["gbids_file"])
    assert isfile(join(settings["asset_dir"], settings["slots_file"])), "%s doesn't exist" % (settings["slots_file"])
    assert isfile(join(settings["asset_dir"], settings["affixes_file"])), "%s doesn't exist" % (settings["affixes_file"])
    assert isfile(join(settings["asset_dir"], settings["currencies_file"])), "%s doesn't exist" % (settings["currencies_file"])

    # load assets
    with open(join(settings["asset_dir"], settings["gbids_file"]), "r") as f:
        gbid_list = load(f)
    with open(join(settings["asset_dir"], settings["slots_file"]), "r") as f:
        slot_list = load(f)
    with open(join(settings["asset_dir"], settings["affixes_file"]), "r") as f:
        affix_list = load(f)
    with open(join(settings["asset_dir"], settings["currencies_file"]), "r") as f:
        currency_list = load(f)

    # parse arguments
    parser = ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-i", "--in-file", type=str, required=True, help="The account file you want to work with")
    parser.add_argument("-o", "--out-file", type=str, default="account_modified.dat", help="The account file you want to output to")
    select_group = parser.add_argument_group("selection")
    select_group.add_argument("-s", "--slot", type=int, default=0, help="The slot ID you want to work with")
    mod_group = parser.add_argument_group("modifications")
    for single in currency_list:
        mod_group.add_argument("--" + single.lower().replace("'", "").replace(" ", "-"), type=int, help="Set the amount of %s" % (single.lower()))
    mod_group.add_argument("--all-currencies", type=int, help="Set all currencies to the given value")
    args = parser.parse_args()

    # make sure the input file exists
    assert isfile(args.in_file), "input file doesn't exist"

    # account
    # decrypt
    with open(args.in_file, "rb") as f:
        account_enc = f.read()
    account_dec = decrypt_save(account_enc)

    # parse
    asd = Account_pb2.SavedDefinition()
    asd.ParseFromString(account_dec)

    # modify account here
    if len(asd.partitions[args.slot].currency_data.currency) > 0:
        for currency_id in range(len(currency_list)):
            currency_name = currency_list[currency_id]
            if len(asd.partitions[args.slot].currency_data.currency) >= (currency_id + 1):
                amt = None
                try:
                    amt = getattr(args, currency_name.lower().replace("'", "").replace(" ", "_"))
                    if not amt and args.all_currencies:
                        amt = args.all_currencies
                except AttributeError:
                    pass
                if amt:
                    print("Set slot %s %s to %s" % (args.slot, currency_name.lower(), amt))
                    asd.partitions[args.slot].currency_data.currency[currency_id].count = amt

    # end account modifications
    account_mod_dec = asd.SerializeToString()
    account_mod_enc = encrypt_save(account_mod_dec)
    # output the modified account
    if args.out_file:
        with open(args.out_file, "wb") as f:
            f.write(account_mod_enc)
    # end account output