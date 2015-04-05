#!/usr/bin/env python
#

import urllib2
import datetime
import time
import os

from apikey import *

URLBASE = 'https://na.api.pvp.net/api/lol/na/v4.1/game/ids?beginDate='

start = datetime.date(year=2015, month=4, day=1)
epoch = int(start.strftime("%s"))
now = int(time.time())
#print epoch
curr = epoch

curr = 1427993700  + 300
#while curr < now:
while True:
    url = '%s%d&api_key=%s' % (URLBASE, curr, APIKEY)

    try:
        f = urllib2.urlopen(url)
        data = f.read()
    except Exception as e:
        print 'exception %s' % e
        print 'url %s' % url
        data = None

    if data is not None:
        # write file
        with open('data/%s' % curr, 'w') as f:
            f.write(data)
        print '%s  wrote %s, data: %s' % (time.strftime("%I:%M:%S"), curr, len(data))

    time.sleep(300)
    curr = curr + 300   # 5 minutes


