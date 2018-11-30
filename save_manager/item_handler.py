import db
from settings import gbid_list
import tkinter as tk


def gbid_to_str(gbid):
    try:
        gbid_return = gbid_list[str(gbid)]
    except KeyError:
        gbid_return = 'Unknown Item - {}'.format(gbid)
    return gbid_return


def affix_to_str(affix):
    try:
        affix_return = db.get_affix_from_id(affix)[0][3]
    except IndexError:
        affix_return = 'Unknown Affix {}'.format(affix)
    return affix_return


def decode_single_item(item):
    enchanted = False
    decoded_item = {}
    gbid = str(item.generator.gb_handle.gbid)
    decoded_gbid = gbid_to_str(gbid)
    if isinstance(decoded_gbid, dict):
        decoded_item['name'] = decoded_gbid['name']
        decoded_item['category'] = decoded_gbid['category']
    else:
        decoded_item['name'] = decoded_gbid
        decoded_item['category'] = 'Unknown Category'
    decoded_item['affixes'] = []

    try:
        enchanted = (int(item.generator.enchanted_affix_old), int(item.generator.enchanted_affix_new))
        if enchanted[0] == -1:
            enchanted = False
    except AttributeError:
        pass

    for affix in item.generator.base_affixes:
        desc = tk.StringVar(value=affix_to_str(affix))
        decoded_item['affixes'].append((affix, desc))

    decoded_item['item'] = item
    if enchanted:
        decoded_item['enchanted'] = []
        decoded_item['enchanted'].append(enchanted)
        decoded_item['enchanted'].append(tk.StringVar(value=affix_to_str(enchanted[1])))
    return decoded_item


def decode_itemlist(itemlist):
    item_out = []
    for item in itemlist:
        item_out.append(decode_single_item(item))
    return item_out

