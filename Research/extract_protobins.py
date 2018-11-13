#!/usr/bin/env python3

from os.path import join, isfile
from binascii import hexlify as _hexlify

NSO_PATH = "C://Users/John/Desktop/Everything/Switch/hactool-1.2.1-win/dumped/exefs/main_decompressed.nso"
NSO_PROTO_OFFSET = 0xDC1EB4

def hexlify(b: (bytes, bytearray)) -> (bytes, bytearray):
    return _hexlify(b).decode("utf8")

if __name__ == "__main__":
    with open(NSO_PATH, "rb") as nso_file:
        # seek to protobuf file listing
        nso_file.seek(NSO_PROTO_OFFSET)

        total_dumped = 0
        while True:
            # print file offset
            print(hex(nso_file.tell()))

            # read protobuf name
            b = None
            protobuf_name = b""
            while True:
                b = nso_file.read(1)
                if b[0] == 0:
                    break
                protobuf_name += b
            protobuf_name = protobuf_name.decode("utf8", errors="ignore")
            print(protobuf_name)

            # no null-terminator
            #assert nso_file.read(1)[0] == 0, "non-null-terminator found"

            # read compiled name
            b = None
            compiled_name = b""
            while True:
                b = nso_file.read(1)
                if b[0] == 0:
                    break
                compiled_name += b
            compiled_name = compiled_name.decode("utf8", errors="ignore")
            print(compiled_name)

            # skip null-terminator
            #assert nso_file.read(1)[0] == 0, "non-null-terminator found"
            if protobuf_name in ["GameMessage.proto", "Leaderboard.proto"]:  # empty
                continue

            if protobuf_name == "Settings.proto": # last one in the list
                break

            # read out the protobin
            protobin = b""
            while True:
                b = nso_file.read(1)
                if b[0] == 0:
                    break
                protobin += b
            #print(hexlify(protobin))
            out_path = join("extracted", protobuf_name + "bin")
            if not isfile(out_path):
                with open(out_path, "wb") as f:
                    f.write(protobin)
            else:
                print("%s already exists, skipping" % (out_path))

            total_dumped += 1
        print("Dumped %s protobin(s)" % (total_dumped))