import re
import requests
from cache_utils.decorators import cached

DDRAGON_VER_URL = 'http://ddragon.leagueoflegends.com/realms/na.json'
ICON_BASE_URL = 'http://ddragon.leagueoflegends.com/cdn/{0}/img/champion/{1}'
LOADING_BASE_URL = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{0}'

special_names = ['DrMundo', 'KogMaw', 'RekSai']

@cached(60*60)
def version():
    # Get most recent data dragon version
    r = requests.get(DDRAGON_VER_URL)
    ddragon_json = r.json()

    if 'v' in ddragon_json.keys():
        ddragon_ver = ddragon_json['v']
    else:
        print 'ERROR: Could not retrieve most recent Data dragon Version.'
        ddragon_ver = '-1'

    return ddragon_ver

VERSION = version()

def champ_icon_url(image):
    return ICON_BASE_URL.format(VERSION, image)

def champ_loading_url(champ_name):
    # Sanitize champ name
    champ_name = re.sub(r'\W+', '', champ_name)

    if champ_name not in special_names:
        champ_name = champ_name.lower().title()

    # Get default skin
    img = '{0}_0.jpg'.format(champ_name)
    return LOADING_BASE_URL.format(img)
