from django.conf.urls import include, url
from django.contrib import admin
import builds.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'prourfbuilds.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^test$', builds.views.test, name='test'),
    url(r'^.*$', include('builds.urls')),
    url(r'^.*/$', include('builds.urls')),
]
