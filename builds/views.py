from django.shortcuts import render_to_response, render
from django.template import RequestContext
from models import Post

import json
import math
import requests

from collections import OrderedDict

from apikey import APIKEY
from lib import ddragon

def index(request):
    url_base= 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion'
    payload = {'champData': 'image,info', 'api_key': APIKEY}

    return_data = {}

    r = requests.get(url_base, params=payload)
    data = r.json()

    if not data:
        # TODO: make an error page for this.
        return render_to_response('champions.html')

    c_list = data['data']
    for champ_id, champ_info in c_list.iteritems():
        name = c_list[champ_id]['name']
        img_url = ddragon.champ_icon_url(c_list[champ_id]['image']['full'])
        return_data[name] = {'img_url': img_url}

    sorted_data = OrderedDict(sorted(return_data.items()))

    return render_to_response('champions.html', {'data': sorted_data})


def champ_info(request, champ_name):
    return render_to_response('champ_info.html', {'data': champ_name})


def test(request):
    post = Post.objects.create(title='test',
                text='test text')
    post.save()
    Post.objects
    data = Post.objects.to_json()
    return render(request, 'test.html', {'data': data})
