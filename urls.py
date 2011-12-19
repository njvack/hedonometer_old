# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

import texter.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url('', include(texter.urls.urlpatterns)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.PUBLIC_DIR}))
