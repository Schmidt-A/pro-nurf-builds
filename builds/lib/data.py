import operator
import random
import string

from cache_utils.decorators import cached

import ddragon
import riotapi

from static_data import builds
from .. import models

@cached(60*60)
def get_champion(champ_id):
    data = models.Champion.objects(value__championId=champ_id)
    return data.first()

@cached(60*60)
def get_total_matches():
    data = models.Match.objects().count()
    return data

def get_builds(champ_id):
    ret_builds = []

    # get the data
    champ = get_champion(int(champ_id))
    itemslist = get_items(champ_id, data=champ)

    for build in builds:
        new_b = {}
        new_b['name'] = build['name']
        new_b['desc'] = build['desc']
        new_b['icon'] = build['icon']
        new_b['items'] = []
        items = get_build_items(build['name'], champ, itemslist)
        if items is not None:
            build['items'] = items
        for item in build['items']:
            img = item['id'] + '.png'
            item['img_url'] = ddragon.item_url(img)
            new_b['items'].append(item)

        ret_builds.append(new_b)

    return ret_builds

def get_items(champ_id, data=None):
    if data is None:
        data = get_champion(int(champ_id))
    d = data['value']
    winrate = calculate_winrate(d['ibuilt'], d['iwin'], minimum=None)

    items = []
    percent_min = 1
    for i in d['ibuilt']:
        if i == '0':
            continue
        apidata = riotapi.item_data(i)
        if apidata['type'] == riotapi.TYPE_TRINKET:
            continue
        buyrate = d['ibuilt'][i] / d['games'] * 100.0
        if buyrate < percent_min:
            continue
        item = apidata
        item['id'] = i
        item['img_url'] = ddragon.item_url(i + '.png')
        item['buyrate'] = int(d['ibuilt'][i] / d['games'] * 100.0)
        item['winrate'] = int(winrate[i])
        item['ifirst_blood'] = int(d['ifirst_blood'].get(i, 0) / d['ibuilt'][i] * 100.0)
        item['ikills'] = d['ikills'].get(i, 0) / d['ibuilt'][i]
        item['ideaths'] = d['ideaths'].get(i, 0) / d['ibuilt'][i]
        item['iassists'] = d['iassists'].get(i, 0) / d['ibuilt'][i]
        items.append(item)

    return items

def get_build_items(bname, data, items):
    fn_name = name_to_fn(bname)
    items = globals()[fn_name](data, items)
    return items

def name_to_fn(name):
    fn = name.lower()
    fn = fn.translate(None, string.punctuation)
    fn = fn.replace(' ', '_')
    return fn

def get_pickrate(champ_id):
    champ = get_champion(champ_id)
    total = get_total_matches()
    return int(champ['value']['games'] / total * 100.0)

def get_winrate(champ_id):
    champ = get_champion(champ_id)
    return int(champ['value']['win'] / champ['value']['games'] * 100.0)

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

def victorious_build(data, items):
    # process the build here.
    d = data['value']
    sorted_items = sorted(items, key=lambda x: x['winrate'], reverse=True)
    return sorted_items[0:6]

def loser_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['winrate'], reverse=False)
    return sorted_items[0:6]

def guest_list_mvp_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['buyrate'], reverse=True)
    return sorted_items[0:6]

def hhey_what_about_me_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['buyrate'], reverse=False)
    return sorted_items[0:6]

def bloodiest_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['ifirst_blood'], reverse=True)
    return sorted_items[0:6]

def i_am_become_urfdeath_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['ikills'], reverse=True)
    return sorted_items[0:6]

def seppuku_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['ideaths'], reverse=True)
    return sorted_items[0:6]

def team_hero_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['iassists'], reverse=True)
    return sorted_items[0:6]

def am_i_not_merciful_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['ikills'], reverse=False)
    return sorted_items[0:6]

def immortal_build(data, items):
    sorted_items = sorted(items, key=lambda x: x['ideaths'], reverse=False)
    return sorted_items[0:6]

