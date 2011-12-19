# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from texter import views

urlpatterns = patterns('',
    url(r'^incoming$', views.IncomingView.as_view()))
