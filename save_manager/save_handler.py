from os.path import isfile, isdir, join
from settings import HERO_DIR
from sys import getsizeof
from binascii import hexlify as _hexlify

XOR_KEY = 0x305F92D82EC9A01B
BYTE_MAX_VALUE = 255


def truncate(num: int, boundary: int, signed: bool, endian: str = "little") -> int:
    """
    Truncate an int to a given byte boundary
    :param num: the number to truncate
    :param boundary: the byte boundary
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


def hexlify(b: (bytes, bytearray)) -> (bytes, bytearray):
    """
    bytes -> hex
    :param b: the bytes you want to convert to hex
    :return: the hex string representation of the specified bytes
    """
    return _hexlify(b).decode("utf8")


def load_encrypted_file(encrypted_file):
    # TODO: Unify account and hero loading
    assert isfile(encrypted_file), "File {} doesn't exist".format(encrypted_file)
    with open(encrypted_file, 'rb') as f:
        file_enc = f.read()
    return file_enc


def load_hero(hero_id):
    if isdir(join("saves", "Modded", HERO_DIR)):
        last_hero_save_path = join("saves", "Modded", HERO_DIR, hero_id + ".dat")
        if isfile(last_hero_save_path):
            with open(last_hero_save_path, "rb") as f:
                hero_enc = f.read()
            hero_dec = decrypt_save(hero_enc)
            return hero_dec
"""
# print(hsd.items.items)
for single in hsd.items.items:
    for affix in single.generator.base_affixes:
        if str(affix) in AFFIX_LIST:
            print(AFFIX_LIST[str(affix)])
        else:
            print("Unknown Affix: %s" % (affix))
"""


def commit_to_file(data, target):
    with open(target, "wb") as f:
        f.write(data)
    return "Changed written to {}".format(target)