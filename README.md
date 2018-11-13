### A script to encrypt/decrypt and modify Diablo III saves

This script is a WIP for modifying Xbox One, PS4, and Switch saves for Diablo III


An example of how to mod gold would work like this (this is the only thing implemented ATM):

`python -i account.dat -o account_mod.dat --gold 999999999`

```
usage: main.py [-h] -i IN_FILE [-o OUT_FILE] [--gold GOLD]

A script to encrypt/decrypt and modify Diablo III saves

optional arguments:
  -h, --help            show this help message and exit
  -i IN_FILE, --in-file IN_FILE
                        The save file you want to work with
  -o OUT_FILE, --out-file OUT_FILE
                        The save file you want to output to

modifications:
  --gold GOLD           The amount of gold you want your characters to have
```

Credits:
> https://github.com/fry -> Diablo III Protobin Decompiler