from settings import gbid_list
from settings import affixes_list


def gbid_to_str(gbid):
    try:
        gbid_return = gbid_list[str(gbid)]
    except KeyError:
        gbid_return = 'Unknown Item'
    return gbid_return


def affix_to_str(affix):
    try:
        affix_return = affixes_list[str(affix)]
    except KeyError:
        affix_return = {'effect': 'Unknown Affix'}
    return affix_return


def decode_single_item(item):
    decoded_item = {}
    gbid = str(item.generator.gb_handle.gbid)
    decoded_gbid = gbid_to_str(gbid)
    if isinstance(decoded_gbid, dict):
        decoded_item['name'] = decoded_gbid['name']
        decoded_item['category'] = decoded_gbid['category']
    else:
        decoded_item['name'] = decoded_gbid
        decoded_item['category'] = 'Unknown Category'
    decoded_item['affixes'] = [affix_to_str(affix) for affix in item.generator.base_affixes]
    decoded_item['item'] = item
    return decoded_item


def decode_itemlist(itemlist):
    item_out = []
    for item in itemlist:
        item_out.append(decode_single_item(item))

    return item_out
