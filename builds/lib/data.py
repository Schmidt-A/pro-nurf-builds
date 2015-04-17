import operator
import random
import string

import ddragon

from static_data import builds
from .. import models


def get_champion(champ_id):
    data = models.Champion.objects(value__championId=champ_id)
    return data.first()

def get_builds(champ_id):
    ret_builds = []

    # get the data
    champ = get_champion(int(champ_id))

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

def get_items(champ_id, data=None):

    if data is None:
        data = get_champion(int(champ_id))
    d = data['value']
    winrate = calculate_winrate(d['ibuilt'], d['iwin'], minimum=None)
    #winrates = sorted_values(winrate, reverse=True)

    items = []
    percent_min = 1
    for i in d['ibuilt']:
        if i == '0':
            continue
        buyrate = d['ibuilt'][i] / d['games'] * 100.0
        if buyrate < percent_min:
            continue
        item = {}
        item['name'] = 'need name'
        item['id'] = i
        item['img_url'] = ddragon.item_url(i + '.png')
        item['buyrate'] = int(d['ibuilt'][i] / d['games'] * 100.0)
        item['winrate'] = int(winrate[i])
        items.append(item)

    return items

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

def sorted_values(to_sort, reverse=False):
    return sorted(to_sort, key=to_sort.get, reverse=reverse)

def calculate_winrate(built, wins, minimum=0):
    winrate = {}
    for item, nbuilt in built.items():
        if item in wins:
            rate = wins[item] / nbuilt * 100.0
        else:
            rate = 0
        if nbuilt >= minimum:
            winrate[item] = rate
    return winrate

def print_item(items, data, built, msg=None):
    if msg is None:
        msg = ''
    print '--- %s' % msg
    for i in items:
        print '%s : %s  built: %s' % (i, data[i], built[i])
    print '---'

def victorious_build(data):
    # process the build here.
    d = data['value']
    winrate = calculate_winrate(d['ibuilt'], d['iwin'], minimum=40)
    items = sorted_values(winrate, reverse=True)
    print_item(items[0:6], winrate, d['ibuilt'])
    return items[0:6]

def loser_build(data):
    d = data['value']
    winrate = calculate_winrate(d['ibuilt'], d['iwin'], minimum=20)
    items = sorted_values(winrate, reverse=False)
    print_item(items[0:6], winrate, d['ibuilt'])
    return items[0:6]

def guest_list_mvp_build(data):
    items = sorted_values(data['value']['ibuilt'], reverse=True)
    return items[0:6]

def hhey_what_about_me_build(data):
    items = sorted_values(data['value']['ibuilt'], reverse=False)
    return items[0:6]

def bloodiest_build(data):
    items = sorted_values(data['value']['ifirst_blood'], reverse=True)
    return items[0:6]

def i_am_become_urfdeath_build(data):
    items = sorted_values(data['value']['ikills'], reverse=True)
    return items[0:6]

def seppuku_build(data):
    items = sorted_values(data['value']['ideaths'], reverse=True)
    return items[0:6]

def team_hero_build(data):
    items = sorted_values(data['value']['iassists'], reverse=True)
    return items[0:6]

def am_i_not_merciful_build(data):
    pass
def immortal_build(data):
    pass

