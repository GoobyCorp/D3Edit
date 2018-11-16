### A script to encrypt/decrypt and modify Diablo III saves

This script is a WIP for modifying Xbox One, PS4, and Switch saves for Diablo III


An example of how to mod gold would work like this (this is the only thing implemented ATM):

`python D3Edit.py -i account.dat -o account_mod.dat -s 0 --gold 999999999`

```
usage: D3Edit.py [-h] -i IN_FILE [-o OUT_FILE] [-s SLOT] [--gold GOLD]
                 [--blood-shards BLOOD_SHARDS]
                 [--reusable-parts REUSABLE_PARTS] [--arcane-dust ARCANE_DUST]
                 [--veiled-crystals VEILED_CRYSTALS]
                 [--deaths-breath DEATHS_BREATH]
                 [--forgotten-souls FORGOTTEN_SOULS]
                 [--khanduran-runes KHANDURAN_RUNES]
                 [--caldeum-nightshade CALDEUM_NIGHTSHADE]
                 [--arreat-war-tapestries ARREAT_WAR_TAPESTRIES]
                 [--corrupted-angel-flesh CORRUPTED_ANGEL_FLESH]
                 [--westmarch-holy-water WESTMARCH_HOLY_WATER]
                 [--hearts-of-fright HEARTS_OF_FRIGHT]
                 [--vials-of-putridness VIALS_OF_PUTRIDNESS]
                 [--idols-of-terror IDOLS_OF_TERROR]
                 [--leorics-regrets LEORICS_REGRETS]
                 [--vengeful-eyes VENGEFUL_EYES]
                 [--writhing-spines WRITHING_SPINES]
                 [--devils-fangs DEVILS_FANGS]
                 [--all-currencies ALL_CURRENCIES]

A script to encrypt/decrypt and modify Diablo III saves

optional arguments:
  -h, --help
                        show this help message and exit
  -i IN_FILE, --in-file IN_FILE
                        The account file you want to work with
  -o OUT_FILE, --out-file OUT_FILE
                        The account file you want to output to

selection:
  -s SLOT, --slot SLOT
                        The slot ID you want to work with

modifications:
  --gold GOLD           Set the amount of Gold
  --blood-shards BLOOD_SHARDS
                        Set the amount of Blood Shards
  --reusable-parts REUSABLE_PARTS
                        Set the amount of Reusable Parts
  --arcane-dust ARCANE_DUST
                        Set the amount of Arcane Dust
  --veiled-crystals VEILED_CRYSTALS
                        Set the amount of Veiled Crystals
  --deaths-breath DEATHS_BREATH
                        Set the amount of Death's Breath
  --forgotten-souls FORGOTTEN_SOULS
                        Set the amount of Forgotten Souls
  --khanduran-runes KHANDURAN_RUNES
                        Set the amount of Khanduran Runes
  --caldeum-nightshade CALDEUM_NIGHTSHADE
                        Set the amount of Caldeum Nightshade
  --arreat-war-tapestries ARREAT_WAR_TAPESTRIES
                        Set the amount of Arreat War Tapestries
  --corrupted-angel-flesh CORRUPTED_ANGEL_FLESH
                        Set the amount of Corrupted Angel Flesh
  --westmarch-holy-water WESTMARCH_HOLY_WATER
                        Set the amount of Westmarch Holy Water
  --hearts-of-fright HEARTS_OF_FRIGHT
                        Set the amount of Hearts of Fright
  --vials-of-putridness VIALS_OF_PUTRIDNESS
                        Set the amount of Vials of Putridness
  --idols-of-terror IDOLS_OF_TERROR
                        Set the amount of Idols of Terror
  --leorics-regrets LEORICS_REGRETS
                        Set the amount of Leoric's Regrets
  --vengeful-eyes VENGEFUL_EYES
                        Set the amount of Vengeful Eyes
  --writhing-spines WRITHING_SPINES
                        Set the amount of Writhing Spines
  --devils-fangs DEVILS_FANGS
                        Set the amount of Devil's Fangs
  --all-currencies ALL_CURRENCIES
                        Set all currencies to the given value
```

Credits:
> https://github.com/fry -> Diablo III Protobin Decompiler