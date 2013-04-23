from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import DetailView, ListView
from summoner.models import Summoner
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'summoner.views.home', name='home'),
    url(r'^summoner/$', 'summoner.views.index', name='index'),
    url(r'^summoner/(?P<summoner_id>\d+)/$', 'summoner.views.detail', name='detail'),
    url(r'^creation/', 'summoner.views.create', name='create'),
    url(r'^thanks/', 'summoner.views.thanks', name='thanks'),
    url(r'^soup/', 'summoner.views.soup', name='soup'),
    url(r'^superSoup/', 'summoner.views.superSoup', name='superSoup'),
)
