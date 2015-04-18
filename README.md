# pro-nurf-builds
(Should be pro-urf-builds, but we made this before the URF detail change.)

Live demo: http://prourfbuilds.com

Contest Submission for the 2015 Riot Games API Challenge.
Developers:
 - Allisa Schmidt (Tweeks, NA): Front-end design and development, art;
 - Russ Milne (teh crust, NA): Data scraping, data aggregation.

Prerequisites
-------------

MongoDB and pip must be installed. The following python modules must be installed via pip:
 - django
 - pymongo (mongoengine doesn't work with pymongo 3.0)
 - mongoengine
 - django-cache-utils
 - django-bootstrap3
 - RiotWatcher
 - requests

> sudo pip install django pymongo==2.8 mongoengine django-cache-utils RiotWatcher requests django-bootstrap3

Front-End
------------
Pro Urf Builds uses the Django web framework and Bootstrap css/js framework. The website art was created with Paint.NET.
