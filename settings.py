from json import load
from os.path import isfile, join


class BiDict(dict):
    def __init__(self, *args, **kwargs):
        super(BiDict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key)
        super(BiDict, self).__setitem__(key, value)
        self.inverse.setdefault(value, []).append(key)

    def __delitem__(self, key):
        self.inverse.setdefault(self[key],[]).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(BiDict, self).__delitem__(key)


# load settings
with open('settings.json') as f:
    settings = load(f)

# define affix regexes to insert effect values.
affix_regexes = '(?P<wc>X-X|^X | X$)'

# apply settings
ASSET_DIR = settings['directories']['ASSET_DIR']
HERO_DIR = settings['directories']['HERO_DIR']
GBIDS_FILE = settings['files']['GBIDS_FILE']
GBID_CAT_FILE = settings['files']['GBID_CAT_FILE']
AFFIXES_FILE = settings['files']['AFFIXES_FILE']
AFFIXES_SIMPLE_FILE = settings['files']['AFFIXES_SIMPLE_FILE']
CURRENCY_FILE = settings['files']['CURRENCY_FILE']
SLOTS_FILE = settings['files']['SLOTS_FILE']

# make sure assets exist
assert isfile(join(ASSET_DIR, GBIDS_FILE)), "%s doesn't exist" % GBIDS_FILE
assert isfile(join(ASSET_DIR, AFFIXES_FILE)), "%s doesn't exist" % AFFIXES_FILE
assert isfile(join(ASSET_DIR, CURRENCY_FILE)), "%s doesn't exist" % CURRENCY_FILE
assert isfile(join(ASSET_DIR, SLOTS_FILE)), "%s doesn't exist" % SLOTS_FILE
assert isfile(join(ASSET_DIR, GBID_CAT_FILE)), "%s doesn't exist" % GBID_CAT_FILE
assert isfile(join(ASSET_DIR, AFFIXES_SIMPLE_FILE)), "%s doesn't exist" % AFFIXES_SIMPLE_FILE


# load assets
with open(join(ASSET_DIR, GBIDS_FILE), "r") as f:
    gbid_list = load(f)
with open(join(ASSET_DIR, AFFIXES_FILE), "r") as f:
    affixes_list = load(f)
with open(join(ASSET_DIR, SLOTS_FILE), "r") as f:
    SLOT_LIST = load(f)
with open(join(ASSET_DIR, CURRENCY_FILE), "r") as f:
    currency_list = load(f)
with open(join(ASSET_DIR, GBID_CAT_FILE), "r") as f:
    gbid_cat = load(f)
with open(join(ASSET_DIR, AFFIXES_SIMPLE_FILE), "r") as f:
    affix_simple = BiDict(load(f))
