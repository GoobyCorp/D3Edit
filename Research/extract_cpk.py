#!/usr/bin/env python3

import zlib
from os import makedirs
from struct import unpack
from argparse import ArgumentParser
from os.path import isfile, isdir, join, split
from ctypes import Structure, sizeof, c_uint32, c_uint64

CPK_MAGIC = 0xA1B2C3D4

SEEK_START = 0
SEEK_CURRENT = 1
SEEK_END = 2

EXTRACTION_DIR = "cpk_dump"

class HeaderStruct(Structure):
    _fields_ = [
        ("Magic", c_uint32),
        ("Version", c_uint32),
        ("Header08", c_uint64),
        ("Header10", c_uint32),
        ("FileCount", c_uint32),
        ("Header18", c_uint32),
        ("Header1C", c_uint32),
        ("Header20", c_uint32),
        ("Header24", c_uint32),
        ("Header28", c_uint32),
        ("Header2C", c_uint32),
        ("Header30", c_uint32),
        ("Header34", c_uint32),
        ("Header38", c_uint32)
    ]

class CPKFile(object):
    _stream = None

    file_size = None
    header = None
    block_1 = None
    block_2 = None
    block_3 = None
    block_4 = None
    block_5 = None
    file_names = []
    file_offsets = []

    def __init__(self, filename: str) -> None:
        if isfile(filename):
            self._stream = open(filename, "rb")
            self.file_size = self.size()
            self.read_header()
            self.read_block_1()
            self.read_block_2()
            self.read_block_3()
            self.read_block_4()
            self.read_block_5()
            self.read_file_names()
            self.read_files()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._stream is not None:
            self.close()

    def read(self, num: int = 0) -> (bytes, bytearray):
        if num <= 0:
            return self._stream.read()
        return self._stream.read(num)

    def tell(self) -> int:
        return self._stream.tell()

    def seek(self, offset: int, whence: int = SEEK_START) -> None:
        self._stream.seek(offset, whence)

    def close(self) -> None:
        self._stream.close()

    def size(self) -> int:
        curr = self.tell()
        self.seek(0, 2)
        size = self.tell()
        self.seek(curr)
        return size

    def read_header(self) -> None:
        self.header = HeaderStruct.from_buffer_copy(self.read(sizeof(HeaderStruct)))
        assert self.header.Magic == CPK_MAGIC, "invalid CPK magic"
        self.read(4)  # skip 4 for some reason?

    def read_block_1(self) -> None:
        size = 0x40
        size += self.header.Header20
        size += self.header.Header24
        size += self.header.Header28
        size *= self.header.FileCount
        size += 7
        size = size >> 3
        self.block_1 = self.read(size)

    def read_block_2(self) -> None:
        size = self.header.Header2C * self.header.Header18
        size += 7
        size = size >> 3
        self.block_2 = self.read(size)

    def read_block_3(self) -> None:
        a = 0x10000
        b = a * self.header.Header1C
        b = self.file_size - b
        b += 0x3FFF
        c = b >> 0xD
        c = c >> 50
        b += c
        b = b >> 0xE
        size = b * self.header.Header2C
        size += 7
        size = size >> 3
        self.block_3 = self.read(size)

    def read_block_4(self) -> None:
        a = 0x10000
        b = a * self.header.Header1C
        b = self.file_size - b
        b += 0x3FFF
        c = b >> 0xD
        c = c >> 50
        b += c
        b = b >> 0xE
        d = self.header.Header08 + 0x3FFF
        e = d >> 0xD
        e = e >> 50
        d += e
        f = d >> 0xE
        g = self.get_highest_bit(b)
        size = f * g
        size += 7
        size = size >> 3
        self.block_4 = self.read(size)

    def read_block_5(self) -> None:
        self.seek(4, SEEK_CURRENT)  # off by 4 for some reason?
        block_5 = []
        for i in range(self.header.FileCount):
            block_5.append(unpack("<I", self.read(4))[0])
        self.block_5 = block_5

    def read_file_names(self) -> None:
        pos = self.tell()
        for i in range(self.header.FileCount):
            self.seek(pos + self.block_5[i])
            self.file_names.append(self.read_string())

    def read_files(self) -> None:
        pos = self.tell() & 0xFFFF0000
        if self.tell() % 0x10000 != 0:
            pos += 0x10000
        self.seek(pos)
        for i in range(len(self.file_names)):  # while True:
            pos = self.tell()
            (unk_0, unk_1, size) = unpack("<HHH", self.read(6))
            if size == 0:
                break
            print(unk_0)
            print(unk_1)
            print(size)
            self.file_offsets.append([pos + 6, size])
            self.seek(size, SEEK_CURRENT)

    def read_string(self) -> str:
        result = b""
        b = None
        while b != b"\x00":
            b = self.read(1)
            result += b
        return result.rstrip(b"\x00").decode("utf8")

    def get_highest_bit(self, u: int) -> int:
        result = 0
        while u != 0:
            u = u >> 1
            result += 1
        return result

if __name__ == "__main__":
    parser = ArgumentParser(description="A script to list and extract Diablo III CPK files")
    parser.add_argument("-i", "--in-file", type=str, help="The CPK file")
    parser.add_argument("-l", "--list", action="store_true", help="List all files in CPK")
    parser.add_argument("-e", "--extract", nargs="+", help="Extract (a) specific file(s) from the CPK")
    parser.add_argument("-a", "--all", action="store_true", help="Extract all files from the CPK")
    args = parser.parse_args()

    assert isfile(args.in_file), "input CPK doesn't exist"
    #assert (args.list or args.extract or args.all), "no action specified"

    with CPKFile(args.in_file) as cpk:
        if args.list:
            for single in cpk.file_names:
                #if single.startswith("StringList"):
                #    print(single)
                print(single)
            print("Listed %s file(s)" % (len(cpk.file_names)))
        elif args.extract:
            print(args.extract)
        elif args.all:
            print("Extracting all files...")

            print(len(cpk.file_names))
            print(len(cpk.file_offsets))

            #for i in range(len(cpk.file_names)):
            (pos, size) = cpk.file_offsets[0]
            file_name = cpk.file_names[0]
            cpk.seek(pos)
            file_data = cpk.read(size)
            file_dec = zlib.decompress(file_data)
            file_path = split(file_name)
            if len(file_path) > 1:
                mkdir_path = join(EXTRACTION_DIR, file_path[0])
                if not isdir(mkdir_path):
                    makedirs(mkdir_path)
            final_path = join(EXTRACTION_DIR, file_name)
            if "|" in final_path:
                final_path = final_path.split("|", 1)[0]
            print(final_path)
            with open(final_path, "wb") as f:
                f.write(file_dec)
        else:
            parser.print_usage()



