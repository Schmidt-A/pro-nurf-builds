#!/usr/bin/python
#
# - watch the games collection and make a queue of population json requests to
#   make to match-v2.2 riot api requests
# - make sure rate limit isn't triggered.
#
import json
import logging
import os
import pymongo
import Queue
import sys
import time
import threading

from riotwatcher import RiotWatcher

from apikey import *

DB = 'urf'
DJANGODB = 'prourfbuilds'
EXIT = False

logging.basicConfig(filename='populate.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG)

# set up logging to console
"""
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
"""

request_q = Queue.Queue()
queue_ids = []
api = RiotWatcher(APIKEY)

def api_get(req):
    data = None
    logging.debug('getting: %s' % req['fn'].__name__)
    while not api.can_make_request():
        logging.debug('wait 0.5 second to make request')
        time.sleep(0.5)
    try:
        data = req['fn'](*req['args'], **req['kwargs'])
    except Exception as e:
        # TODO handle error code for rate limit and return it
        logging.info('exception getting:%s %s' % (url, e))
    return data

def insert(collection, data):
    logging.debug('insert into %s data len: %s' % (collection, len(json.dumps(data))))
    conn = pymongo.MongoClient()
    db = getattr(conn, DJANGODB)
    coll = getattr(db, collection)
    result = coll.insert(data)
    logging.debug('insert returned %s' % result)
    conn.close()

def request_thread():
    logging.debug('request thread started')
    def main_is_alive():
        for i in threading.enumerate():
            if i.name == "MainThread":
                return i.is_alive()

    while not EXIT and main_is_alive():
        try:
            req = request_q.get_nowait()
        except Queue.Empty as e:
            time.sleep(2)
            continue
        data = api_get(req)
        if data is not None:
            insert(req['coll'], data)
        time.sleep(1)
    logging.debug('thread exiting')

def is_match_downloaded(matchid):
    found = False
    conn = pymongo.MongoClient()
    coll = getattr(conn, DJANGODB).match
    if coll.find_one({'matchId': matchid}):
        found = True
    conn.close()
    return found

def process_games():
    global queue_ids
    conn = pymongo.MongoClient()
    coll = conn.urf.game

    logging.debug('process_games before query')
    # look at one game entry at a time
    game = coll.find_one({'processed': {'$exists': False}})
    if game:
        processed_already = True
        for g in game['games']:
            if not is_match_downloaded(g) and g not in queue_ids:
                processed_already = False
                request_q.put({'coll': 'match',
                                  'fn': api.get_match,
                                  'args': [g],
                                  'kwargs': {'include_timeline': True}})
                queue_ids.append(g)
        if processed_already:
            logging.debug('marking game id %s as processed' % (game['_id']))
            result = coll.update_one({'_id': game['_id']}, {'$set': {'processed':
                True}})
            logging.debug('update result: %s' % result)
    logging.debug('request q size: %s' % request_q.qsize())
    conn.close()

def main():
    # setup request thread
    req_thread = threading.Thread(target=request_thread)
    req_thread.start()

    # watch the mongo collections for new data to populate
    while True:
        process_games()
        logging.info('request queue size: %s' % request_q.qsize())
        # wait between iterations
        time.sleep(30)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.debug('main exiting')
        EXIT = True
        sys.exit(1)
