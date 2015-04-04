#!/usr/bin/python
#
# insert pulled urf games into mongodb
#
#

import json
import os
import pymongo
import time

path = 'data'
dest = 'inserted'

while True:
    conn = pymongo.Connection()
    coll = conn.urf.game
    for root, dirs, files in os.walk(path):
        for f in files:
            data = None
            with open(os.path.join(path, f)) as handle:
                data = handle.read()
            if data is not None:
                data = '{"games": %s}' % data
                print coll.insert(json.loads(data))
                os.rename(os.path.join(path, f), os.path.join(dest, f))
    conn.disconnect()
    time.sleep(300)




