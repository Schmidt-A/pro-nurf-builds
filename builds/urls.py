from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('builds.views',
        url(r'^champion/(.*)$', views.champ_info, name='champ_info'),
        url(r'^test$', views.test, name='test'),
        url(r'^$', views.index, name='index'),
        )

