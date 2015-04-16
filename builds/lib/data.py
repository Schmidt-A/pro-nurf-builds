import random
import string

import ddragon

from static_data import builds
from .. import models


def get_champion(champ_id):
    data = models.Champion.objects(_id=champ_id)
    return data

def get_builds(champ_id):
    ret_builds = []

    # get the data
    champ = get_champion(champ_id)

    for build in builds:
        new_b = {}
        new_b['name'] = build['name']
        new_b['desc'] = build['desc']
        new_b['icon'] = build['icon']
        new_b['items'] = []
        items = get_build_items(build['name'], champ)
        if items is not None:
            build['items'] = items
        for item in build['items']:
            img = item + '.png'
            ddragon_img_url = ddragon.item_url(img)
            new_b['items'].append(ddragon_img_url)

        ret_builds.append(new_b)

    return ret_builds

def get_items(champ_id):
    # Back end call
    items = []
    for i in range(0, 30):
        item = {}
        item['name'] = 'Boots of Speed'
        item['id'] = '1001'
        item['buyrate'] = random.randint(1, 100)
        item['winrate'] = random.randint(1, 100)
        items.append(item)

    ret_items = []

    for item in items:
        new_i = {}
        new_i['name'] = item['name']
        new_i['img_url'] = ddragon.item_url(item['id'] + '.png')
        new_i['buyrate'] = item['buyrate']
        new_i['winrate'] = item['winrate']
        ret_items.append(new_i)

    return ret_items

def get_build_items(bname, data):
    fn_name = name_to_fn(bname)
    items = globals()[fn_name](data)
    return items

def name_to_fn(name):
    fn = name.lower()
    fn = fn.translate(None, string.punctuation)
    fn = fn.replace(' ', '_')
    return fn

def get_pickrate(champ_id):
    return 69

def get_winrate(champ_id):
    return 69

def get_banrate(champ_id):
    return 69

def victorious_build(data):
    # process the build here.
    return ['1001', '3709', '1001', '3709', '1001', '3709']

def loser_build(data):
    pass
def guest_list_mvp_build(data):
    pass
def hhey_what_about_me_build(data):
    pass
def bloodiest_build(data):
    pass
def i_am_become_urfdeath_build(data):
    pass
def seppuku_build(data):
    pass
def team_hero_build(data):
    pass
def am_i_not_merciful_build(data):
    pass
def immortal_build(data):
    pass

