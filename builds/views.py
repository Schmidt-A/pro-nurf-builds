from django.shortcuts import render_to_response, render
from django.template import RequestContext
from models import Champion

from collections import OrderedDict

from lib import data, ddragon, riotapi

def index(request):
    return_data = {}
    c_list = riotapi.champs_data()

    if not c_list:
        # TODO: make an error page for this.
        return render_to_response('champions.html')

    for champ_id, champ_info in c_list.iteritems():
        cur_champ = c_list[champ_id]

        name = cur_champ['name']
        img_url = ddragon.champ_icon_url(cur_champ['image']['full'])

        return_data[name] = {
                'img_url': img_url,
                }

    sorted_data = OrderedDict(sorted(return_data.items()))

    return render_to_response('champions.html', {'data': sorted_data})


def champ_info(request, name):
    champ = riotapi.champ_data(name)
    title = champ['title']
    loading_url = ddragon.champ_loading_url(champ['key'])
    winrate = data.get_winrate(champ['id'])
    pickrate = data.get_pickrate(champ['id'])
    banrate = data.get_banrate(champ['id'])
    builds = data.get_builds(champ['id'])
    items = data.get_items(champ['id'])

    return render_to_response('champ_info.html',
            {
                'name': name,
                'title': title,
                'img_url': loading_url,
                'winrate': winrate,
                'pickrate': pickrate,
                'banrate': banrate,
                'builds': builds,
                'items': items
            })

