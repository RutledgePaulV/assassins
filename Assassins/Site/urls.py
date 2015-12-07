from django.conf.urls import patterns, url
from Site.views import *


urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^geek/$', geek, name='geek'),
                       url(r'^thanks/$', thanks, name='thanks'),
                       url(r'^contact/$', contact, name='contact'),
)
