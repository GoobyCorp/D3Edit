from json import load
from os.path import isfile, join


dbfile = 'db/local.db'

# load settings
with open('settings.json') as f:
    settings = load(f)

# apply settings
ASSET_DIR = settings['directories']['ASSET_DIR']
HERO_DIR = settings['directories']['HERO_DIR']
GBIDS_FILE = settings['files']['GBIDS_FILE']
GBID_CAT_FILE = settings['files']['GBID_CAT_FILE']
SLOTS_FILE = settings['files']['SLOTS_FILE']

# make sure assets exist
assert isfile(join(ASSET_DIR, GBIDS_FILE)), "%s doesn't exist" % GBIDS_FILE
assert isfile(join(ASSET_DIR, SLOTS_FILE)), "%s doesn't exist" % SLOTS_FILE
assert isfile(join(ASSET_DIR, GBID_CAT_FILE)), "%s doesn't exist" % GBID_CAT_FILE


# load assets
with open(join(ASSET_DIR, GBIDS_FILE), "r") as f:
    gbid_list = load(f)
with open(join(ASSET_DIR, SLOTS_FILE), "r") as f:
    SLOT_LIST = load(f)
with open(join(ASSET_DIR, GBID_CAT_FILE), "r") as f:
    gbid_cat = load(f)
