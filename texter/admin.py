# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.contrib import admin
from django import forms
from . import models

TEXTAREA_ATTRS = {'cols': 100, 'rows': 4}


class QuestionPartForm(forms.ModelForm):

    message_text = forms.CharField(
        widget=forms.Textarea(attrs=TEXTAREA_ATTRS))

    class Meta:
        model = models.QuestionPart


class QuestionPartInline(admin.TabularInline):

    model = models.QuestionPart

    extra = 1

    form = QuestionPartForm


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


class ExperimentForm(forms.ModelForm):

    unknown_participant_message = forms.CharField(
        widget=forms.Textarea(attrs=TEXTAREA_ATTRS))

    no_response_needed_message = forms.CharField(
        widget=forms.Textarea(attrs=TEXTAREA_ATTRS))

    bad_answer_message = forms.CharField(
        widget=forms.Textarea(attrs=TEXTAREA_ATTRS))

    class Meta:
        model = models.Experiment


class ExperimentAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Setup', {'fields':
            (
                ('name', 'url_slug'),
                ('backend', ),
                ('experiment_length_days',
                'max_samples_per_day',
                'min_time_between_samples',
                'max_time_between_samples'),
                ('accepted_answer_pattern',
                'answer_ignores_case'),
                ('unknown_participant_message',
                'no_response_needed_message',
                'bad_answer_message'))}), )

    readonly_fields = ['url_slug', ]

    inlines = [
        QuestionPartInline,
        ParticipantInline]

    form = ExperimentForm


class BackendAdmin(admin.ModelAdmin):

    readonly_fields = ['delegate_classname', 'delegate_pk', 'name']


class TextMessageAdmin(admin.ModelAdmin):

    pass

admin.site.register(models.Experiment, ExperimentAdmin)

admin.site.register(models.Backend, BackendAdmin)

admin.site.register(models.Participant, ParticipantAdmin)

admin.site.register(models.IncomingTextMessage, TextMessageAdmin)

admin.site.register(models.OutgoingTextMessage, TextMessageAdmin)
