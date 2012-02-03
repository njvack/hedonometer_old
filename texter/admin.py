# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.contrib import admin
from . import models


class QuestionPartInline(admin.TabularInline):

    model = models.QuestionPart

    extra = 1


class ParticipantInline(admin.TabularInline):

    model = models.Participant

    extra = 1


class TaskDayInline(admin.TabularInline):

    model = models.TaskDay

    extra = 1


class ScheduledSampleInline(admin.TabularInline):

    model = models.ScheduledSample

    extra = 1


class ParticipantAdmin(admin.ModelAdmin):

    inlines = [
        TaskDayInline,
        ScheduledSampleInline]


class ExperimentAdmin(admin.ModelAdmin):

    readonly_fields = ['url_slug', ]

    inlines = [
        QuestionPartInline,
        ParticipantInline]


class BackendAdmin(admin.ModelAdmin):

    readonly_fields = ['delegate_classname', 'delegate_pk', 'name']


class TextMessageAdmin(admin.ModelAdmin):

    pass

admin.site.register(models.Experiment, ExperimentAdmin)

admin.site.register(models.Backend, BackendAdmin)

admin.site.register(models.Participant, ParticipantAdmin)

admin.site.register(models.IncomingTextMessage, TextMessageAdmin)

admin.site.register(models.OutgoingTextMessage, TextMessageAdmin)
