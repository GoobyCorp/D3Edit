### A script to encrypt/decrypt and modify Diablo III saves

This script is a WIP for modifying Xbox One, PS4, and Switch saves for Diablo III


An example of how to mod gold would work like this (this is the only thing implemented ATM):

`python D3Edit.py -i account.dat -o account_mod.dat --gold 999999999`

```
usage: D3Edit.py [-h] -i IN_FILE [-o OUT_FILE] [--gold GOLD]
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
  -h, --help            show this help message and exit
  -i IN_FILE, --in-file IN_FILE
                        The account file you want to work with
  -o OUT_FILE, --out-file OUT_FILE
                        The account file you want to output to

modifications:
  --gold GOLD           The amount of gold you want your characters to have
  --blood-shards BLOOD_SHARDS
                        The amount of blood shards you want your characters to have
  --reusable-parts REUSABLE_PARTS
                        The amount of reusable parts you want your characters to have
  --arcane-dust ARCANE_DUST
                        The amount of arcane dust you want your characters to have
  --veiled-crystals VEILED_CRYSTALS
                        The amount of veiled crystals you want your characters to have
  --deaths-breath DEATHS_BREATH
                        The amount of deaths breath you want your characters to have
  --forgotten-souls FORGOTTEN_SOULS
                        The amount of forgotten souls you want your characters to have
  --khanduran-runes KHANDURAN_RUNES
                        The amount of Khanduran runes you want your characters to have
  --caldeum-nightshade CALDEUM_NIGHTSHADE
                        The amount of Caldeum nightshade you want your characters to have
  --arreat-war-tapestries ARREAT_WAR_TAPESTRIES
                        The amount of Arret War tapestries you want your characters to have
  --corrupted-angel-flesh CORRUPTED_ANGEL_FLESH
                        The amount of corrupted angel flesh you want your characters to have
  --westmarch-holy-water WESTMARCH_HOLY_WATER
                        The amount of Westmarch holy water you want your characters to have
  --hearts-of-fright HEARTS_OF_FRIGHT
                        The amount of hearts of fright you want your characters to have
  --vials-of-putridness VIALS_OF_PUTRIDNESS
                        The amount of vials of putridness you want your characters to have
  --idols-of-terror IDOLS_OF_TERROR
                        The amount of idols of terror you want your characters to have
  --leorics-regrets LEORICS_REGRETS
                        The amount of Leoric's regrets you want your characters to have
  --vengeful-eyes VENGEFUL_EYES
                        The amount of vengeful eyes you want your characters to have
  --writhing-spines WRITHING_SPINES
                        The amount of writhing spines you want your characters to have
  --devils-fangs DEVILS_FANGS
                        The amount of devil's fangs you want your characters to have
  --all-currencies ALL_CURRENCIES
                        Set all currencies to the given value
```

Credits:
> https://github.com/fry -> Diablo III Protobin Decompiler