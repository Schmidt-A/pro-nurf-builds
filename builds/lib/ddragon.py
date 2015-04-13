import requests

DDRAGON_VER_URL = 'http://ddragon.leagueoflegends.com/realms/na.json'
IMG_BASE_URL = 'http://ddragon.leagueoflegends.com/cdn/{0}/img/champion/{1}'

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
    return IMG_BASE_URL.format(VERSION, image)
