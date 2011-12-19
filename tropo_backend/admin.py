# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.contrib import admin
from . import models


class TropoBackendAdmin(admin.ModelAdmin):

    readonly_fields = ['qualified_classname']

admin.site.register(models.TropoBackend, TropoBackendAdmin)
