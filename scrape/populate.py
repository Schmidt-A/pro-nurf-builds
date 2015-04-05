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
import urllib2


from apikey import *

DB = 'urf'
EXIT = False

logging.basicConfig(filename='populate.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG)

request_q = Queue.Queue()

def api_get(url):
    data = None
    logging.debug('getting: %s' % url)
    try:
        f = urllib2.urlopen(url)
        data = f.read()
    except Exception as e:
        # TODO handle error code for rate limit and return it
        logging.info('exception getting:%s %s' % (url, e))
    return data

def insert(coll, data):
    logging.debug('insert into %s data len: %s' % (coll, len(data)))
    #TODO

def request_thread():
    logging.debug('request thread started')
    while not EXIT:
        try:
            coll, url = request_q.get_nowait()
        except Queue.Empty as e:
            time.sleep(2)
            continue
        data = api_get(url)
        if data is not None:
            insert(col, data)
        time.sleep(2)
    logging.debug('thread exiting')

def watch_games():
    #TODO logic to query mongo and make request jobs
    pass

def main():
    # setup request thread
    req_thread = threading.Thread(target=request_thread)
    req_thread.start()

    # watch the mongo collections for new data to populate
    while True:

        logging.info('request queue size: %s' % request_q.qsize())
        # wait between iterations
        time.sleep(90)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.debug('main exiting')
        EXIT = True
        sys.exit(1)
