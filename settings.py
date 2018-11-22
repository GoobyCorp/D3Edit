from json import load
from os.path import isfile, join

# load settings
with open('settings.json') as f:
    settings = load(f)

# apply settings
ASSET_DIR = settings['directories']['ASSET_DIR']
HERO_DIR = settings['directories']['HERO_DIR']
GBIDS_FILE = settings['files']['GBIDS_FILE']
AFFIXES_FILE = settings['files']['AFFIXES_FILE']
CURRENCY_FILE = settings['files']['CURRENCY_FILE']
SLOTS_FILE = settings['files']['SLOTS_FILE']

# make sure assets exist
assert isfile(join(ASSET_DIR, GBIDS_FILE)), "%s doesn't exist" % GBIDS_FILE
assert isfile(join(ASSET_DIR, AFFIXES_FILE)), "%s doesn't exist" % AFFIXES_FILE
assert isfile(join(ASSET_DIR, CURRENCY_FILE)), "%s doesn't exist" % CURRENCY_FILE
# load assets
with open(join(ASSET_DIR, GBIDS_FILE), "r") as f:
    gbid_list = load(f)
with open(join(ASSET_DIR, AFFIXES_FILE), "r") as f:
    AFFIX_LIST = load(f)
with open(join(ASSET_DIR, SLOTS_FILE), "r") as f:
    SLOT_LIST = load(f)
with open(join(ASSET_DIR, CURRENCY_FILE), "r") as f:
    currency_list = load(f)