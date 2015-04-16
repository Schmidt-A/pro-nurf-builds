from sample_data import builds
import random
import ddragon

def get_builds(champ_id):
    # BACK END DATA CALL HERE TO REPLACE BUILDS FROM SAMPLE DATA
    ret_builds = []

    for build in builds:
        new_b = {}
        new_b['name'] = build['name']
        new_b['desc'] = build['desc']
        new_b['icon'] = build['icon']
        new_b['items'] = []
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


def get_pickrate(champ_id):
    return 69

def get_winrate(champ_id):
    return 69

def get_banrate(champ_id):
    return 69
