#!/usr/bin/env python3

from os import walk
from os.path import join, isfile

if __name__ == "__main__":
    for (one, two, three) in walk("decompiled"):
        for single in three:
            if single.endswith(".proto"):
                file_path = join(one, single)
                if isfile(file_path):
                    with open(file_path, "r") as fr:
                        file_data = fr.read()
                    with open(file_path, "w") as fw:
                        if "syntax = \"proto2\";" not in file_data:
                            file_data = "syntax = \"proto2\"\n;" + file_data
                            fw.write(file_data)