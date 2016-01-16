from django.conf.urls import patterns, include, url
from django.contrib import admin
from lk.views import *

urlpatterns = patterns('',
    url(r'^$', 'lk.views.home', name='home'),
)
