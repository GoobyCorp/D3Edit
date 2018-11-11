#!/usr/bin/env python3

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
    pass