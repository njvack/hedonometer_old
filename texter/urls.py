# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from texter import views

urlpatterns = patterns('',
    url(r'^incoming/(?P<url_slug>\w+)$', 'texter.views.incoming'),
    url(r'^samples/(?P<url_slug>\w+)\.csv$', 'texter.views.samples_csv'),
    url(r'^outgoing_messages/(?P<url_slug>\w+)\.csv$', 
        'texter.views.outgoing_texts_csv'), 
    url(r'^incoming_messages/(?P<url_slug>\w+)\.csv$', 
        'texter.views.incoming_texts_csv'),)
