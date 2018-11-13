#!/usr/bin/env python3

from os.path import isfile
from argparse import ArgumentParser
from ctypes import Structure, sizeof, c_ubyte, c_uint16, c_uint32, c_uint64

from StreamIO import *

GAM_MAGIC = 0xDEADBEEF

class GAMHeader(Structure):
    _fields_ = [
        ("Magic", c_uint32),
        ("a", c_ubyte),
        ("b", c_ubyte)
    ]

class GAMFile(object):
    sio = None

    header = None

    def __init__(self, filename: str) -> None:
        if isfile(filename):
            f = open(filename, "rb")
            self.sio = StreamIO(f)
            self.read_header()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sio.close()

    def read_header(self) -> None:
        self.header = self.sio.read_struct(GAMHeader)

if __name__ == "__main__":
    with GAMFile("GameBalance/AffixList.gam") as gam:
        print(gam.header.Magic)
        print(gam.header.a)
        print(gam.header.b)