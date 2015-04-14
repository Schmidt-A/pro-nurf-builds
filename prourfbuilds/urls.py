from django.conf.urls import include, url, patterns
from django.contrib import admin
import builds.views

urlpatterns = patterns('',
        (r'^', include('builds.urls')),
        )
