import requests

from cache_utils.decorators import cached

from apikey import APIKEY
import ddragon

URL_BASE = 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/{0}'

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
