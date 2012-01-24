# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.contrib import admin
from . import models


class ExperimentAdmin(admin.ModelAdmin):

    readonly_fields = ['url_slug', ]


class BackendAdmin(admin.ModelAdmin):

    readonly_fields = ['delegate_classname', 'delegate_pk', 'name']

admin.site.register(models.Experiment, ExperimentAdmin)

admin.site.register(models.Backend, BackendAdmin)

admin.site.register(models.Participant, admin.ModelAdmin)
