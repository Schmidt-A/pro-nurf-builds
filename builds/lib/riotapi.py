import requests

from cache_utils.decorators import cached

from apikey import APIKEY
import ddragon

URL_BASE = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/{0}'
TYPE_BOOT = 'Boots'
TYPE_TRINKET = 'Trinket'
TYPE_GENERAL = 'General'

@cached(60*60)
def champs_data():
    payload = {'champData': 'altimages,image,info', 'api_key': APIKEY}
    url = URL_BASE.format('champion')

    r = requests.get(url, params=payload)
    data = r.json()

    if not data:
        return None

    return data['data']

def champ_data(name):
    data = champs_data()

    # Get info by name
    champ_info = lambda x: [data[cid] for cid in data if data[cid]['name'] == x]
    return champ_info(name)[0]

@cached(60*60)
def items_data():
    payload = {'itemListData': 'groups,image,tags', 'api_key': APIKEY}
    url = URL_BASE.format('item')

    r = requests.get(url, params=payload)
    data = r.json()['data']
    return data

def item_data(item_id):
    data = items_data()[item_id]

    item = {}
    item['id'] = item_id
    item['type'] = TYPE_GENERAL

    # Check item type... Really messy because the API data is messy.
    if 'tags' in data:
        if 'Boots' in data['tags']:
            item['type'] = TYPE_BOOT
        elif 'Trinket' in data['tags']:
            item['type'] = TYPE_TRINKET
    elif 'group' in data:
        if str(data['group']).startswith('Boots'):
            item['type'] = TYPE_BOOT

    item['desc'] = data['description']
    item['name'] = data['name']

    return item
