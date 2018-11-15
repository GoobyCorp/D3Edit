### A script to encrypt/decrypt and modify Diablo III saves

This script is a WIP for modifying Xbox One, PS4, and Switch saves for Diablo III


An example of how to mod gold would work like this (this is the only thing implemented ATM):

`python D3Edit.py -i account.dat -o account_mod.dat --gold 999999999`

```
usage: D3Edit.py [-h] -i IN_FILE [-o OUT_FILE] [--gold GOLD]
                 [--blood-shards BLOOD_SHARDS] [--platinum PLATINUM]
                 [--reusable-parts REUSABLE_PARTS] [--arcane-dust ARCANE_DUST]
                 [--veiled-crystals VEILED_CRYSTALS]
                 [--deaths-breath DEATHS_BREATH]
                 [--forgotten-souls FORGOTTEN_SOULS]
                 [--khanduran-runes KHANDURAN_RUNES]
                 [--caldeum-nightshade CALDEUM_NIGHTSHADE]
                 [--arreat-war-tapestries ARREAT_WAR_TAPESTRIES]
                 [--corrupted-angel-flesh CORRUPTED_ANGEL_FLESH]
                 [--westmarch-holy-water WESTMARCH_HOLY_WATER]
                 [--demon-organ-diablo DEMON_ORGAN_DIABLO]
                 [--demon-organ-ghom DEMON_ORGAN_GHOM]
                 [--demon-organ-siege-breaker DEMON_ORGAN_SIEGE_BREAKER]
                 [--demon-organ-skeleton-king DEMON_ORGAN_SKELETON_KING]
                 [--demon-organ-eye DEMON_ORGAN_EYE]
                 [--demon-organ-spinal-cord DEMON_ORGAN_SPINAL_CORD]
                 [--demon-organ-teeth DEMON_ORGAN_TEETH]

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
  --platinum PLATINUM   The amount of platinum you want your characters to have
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
  --demon-organ-diablo DEMON_ORGAN_DIABLO
                        The amount of Diablo demon organs you want your characters to have
  --demon-organ-ghom DEMON_ORGAN_GHOM
                        The amount of Ghom demon organs you want your characters to have
  --demon-organ-siege-breaker DEMON_ORGAN_SIEGE_BREAKER
                        The amount of siege breaker demon organs you want your characters to have
  --demon-organ-skeleton-king DEMON_ORGAN_SKELETON_KING
                        The amount of skeleton king demon organs you want your characters to have
  --demon-organ-eye DEMON_ORGAN_EYE
                        The amount of eye demon organs you want your characters to have
  --demon-organ-spinal-cord DEMON_ORGAN_SPINAL_CORD
                        The amount of spinal cord demon organs you want your characters to have
  --demon-organ-teeth DEMON_ORGAN_TEETH
                        The amount of teeth demon organs you want your characters to have
```

Credits:
> https://github.com/fry -> Diablo III Protobin Decompiler