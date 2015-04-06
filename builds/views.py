from django.shortcuts import render_to_response, render
from django.template import RequestContext
from models import Post
import urllib2
import json

def index(request):
    key = 'c881ae04-2d79-46f4-8857-900a0ba71f5e'
    urlbase= 'https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=image,info'
    url = '%s&api_key=%s' % (urlbase, key)

    ddragon_ver_url = 'http://ddragon.leagueoflegends.com/realms/na.json'
    ddragon_img_base = 'http://ddragon.leagueoflegends.com/cdn/{0}/img/champion/{1}'

    return_data = {}

    # Get most recent data dragon version
    try:
        f = urllib2.urlopen(ddragon_ver_url)
        ddata = f.read()
        ddata = json.loads(ddata)
        ddragon_ver = ddata['v']
    except Exception as e:
        print 'Exception:', e
        ddragon_ver = None

    if not ddragon_ver:
        # TODO: make an error page for this.
        return render_to_response('champions.html')


    try:
        f = urllib2.urlopen(url)
        data = f.read()
        data = json.loads(data)
    except Exception as e:
        print 'Exception:', e
        print 'url:', url
        data = None

    if not data:
        # TODO: make an error page for this.
        return render_to_response('champions.html')

    c_list = data['data']
    for champ_id, champ_info in c_list.iteritems():
        name = c_list[champ_id]['name']
        image = c_list[champ_id]['image']['full']
        img_url = ddragon_img_base.format(ddragon_ver, image)
        return_data[name] = {'img_url': img_url}

    print return_data

    return render_to_response('champions.html', {'data': return_data})



def test(request):
    post = Post.objects.create(title='test',
                text='test text')
    post.save()
    Post.objects
    data = Post.objects.to_json()
    return render(request, 'test.html', {'data': data})
