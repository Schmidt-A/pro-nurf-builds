# pro-nurf-builds
(Should be pro-urf-builds, but we made this before the URF detail change.)

Live demo: http://prourfbuilds.com

Contest Submission for the 2015 Riot Games API Challenge.
Developers:
 - Allisa Schmidt (Tweeks, NA): Front-end design and development, art;
 - Russ Milne (teh crust, NA): Data scraping, data aggregation.

## Prerequisites

MongoDB and pip must be installed. The following python modules must be installed via pip:
 - django
 - pymongo (mongoengine doesn't work with pymongo 3.0)
 - mongoengine
 - django-cache-utils
 - django-bootstrap3
 - RiotWatcher
 - requests

> sudo pip install django pymongo==2.8 mongoengine django-cache-utils RiotWatcher requests django-bootstrap3

## Front-End

### TL;DR
Pro Urf Builds uses the Django web framework and Bootstrap css/js framework. The website art was created with Paint.NET.

A few utility scripts can be found in builds/lib/
 - data.py - translates back-end data into front-end friendly dictionaries
 - ddragon.py - little API to get static images from Riot's Data Dragon service
 - riotapi.py - tiny API to run pertinent Riot API requests

### Future
Due to timing, the front end CSS and templates are definitely not as clean as they could be. Refining those would make the app much more scaleable.


## Back-End

### Data Collection
A series of quick and dirty python scripts retrieved the URF games from the URF endpoint

scrape/
 - pull.py - periodically pulled the gameid data from the challenge endpoint
 - insert.py - insert the json files from pull.py and insert them into mongodb
 - populate.py - watch the games collection in mongo and populate the match collection
              using the match API endpoint with RiotWatcher api library

### Aggregation
Using MongoDb's mapReduce aggregation the match data was combined by champion and item statistics to provide django a set of aggregated data to form the builds and item statistics per champion

### Future
The data collection scripts need a rewrite into a clean service or cron command which in turn could trigger the aggregation.  Aggregation on an ongoing basis could be modified to use an incremental approach.
