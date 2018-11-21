#!/usr/bin/env python3

from os.path import isfile
from ctypes import Structure, sizeof, c_uint32

from StreamIO import *

class STLHeader(Structure):
    _fields_ = [
        ("magic", c_uint32),
        ("entry_start", c_uint32)
    ]

class STLFile(object):
    _stream = None

    _header = None

    def __init__(self, filename: str) -> None:
        if isfile(filename):
            f = open(filename, "rb")
            self._stream = StreamIO(f)
            self.read_header()
            self.read_entries()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stream.close()

    def read_header(self) -> None:
        self._header = STLHeader.from_buffer_copy(self._stream.read(sizeof(STLHeader)))
        assert self._header.magic == 0xDEADBEEF, "invalid magic"

    def read_entries(self):
        self._stream.seek(self._header.entry_start)
        self._stream.seek(self._stream.read_uint32())
        print(self._stream.read(8))

if __name__ == "__main__":
    with STLFile("StringList/Affixes.stl") as stl:
        pass