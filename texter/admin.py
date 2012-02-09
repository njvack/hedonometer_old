# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.contrib import admin
from django import forms
from . import models

TEXTAREA_ATTRS = {'cols': 100, 'rows': 4}


def make_link(link_text, instance_url_method):

    def link_to_url(admin, instance):
        url = getattr(instance, instance_url_method)()
        return '<a href="%s">%s</a>' % (url, link_text)
    link_to_url.allow_tags = True
    return link_to_url


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

    full_edit_link = make_link('Edit participant', 'admin_edit_url')

    readonly_fields = ['stopped', 'full_edit_link']

    fields = ['phone_number', 'id_code', 'start_date',
        'normal_earliest_message_time', 'normal_latest_message_time',
        'full_edit_link']

    can_delete = False

    extra = 1


class TaskDayInline(admin.TabularInline):

    model = models.TaskDay

    extra = 1


class ScheduledSampleInline(admin.TabularInline):

    model = models.ScheduledSample

    ordering = ['-scheduled_at']

    readonly_fields = [
        'task_day', 'answered_by', 'sent_at', 'answered_at']

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
                ('samples_csv_url', 'outgoing_csv_url', 'incoming_csv_url'),
                ('incoming_admin_link', 'outgoing_admin_link'),
                ('experiment_length_days',
                'max_samples_per_day',
                'min_time_between_samples',
                'max_time_between_samples'),
                ('accepted_answer_pattern',
                'answer_ignores_case'),
                ('unknown_participant_message',
                'no_response_needed_message',
                'bad_answer_message'))}), )


    samples_csv_url = make_link('Samples CSV', 'get_samples_csv_url')

    outgoing_csv_url = make_link(
        'Outgoing messages CSV', 'get_outgoing_csv_url')

    incoming_csv_url = make_link(
        'Incoming messages CSV', 'get_incoming_csv_url')

    incoming_admin_link = make_link(
        'Incoming text messages', 'get_incoming_admin_url')

    outgoing_admin_link = make_link(
        'Outgoing text messages', 'get_outgoing_admin_url')

    readonly_fields = ['url_slug', 'samples_csv_url', 'outgoing_csv_url',
        'incoming_csv_url', 'incoming_admin_link', 'outgoing_admin_link']

    inlines = [
        QuestionPartInline,
        ParticipantInline]

    form = ExperimentForm


class BackendAdmin(admin.ModelAdmin):

    readonly_fields = ['delegate_classname', 'delegate_pk', 'name']


class TextMessageAdmin(admin.ModelAdmin):

    actions = None

    ordering = ['-sent_at']

    list_filter = ['experiment', 'from_phone', 'to_phone', 'sent_at']

    def has_add_permission(self, req, obj=None):
        return False

    def has_delete_permission(self, req, obj=None):
        return False


class IncomingTextMessageAdmin(TextMessageAdmin):

    list_display = ['pk', 'to_phone', 'from_phone', 'message_text', 'sent_at',
        'received_at']

    readonly_fields = ['to_phone', 'from_phone', 'message_text', 'sent_at',
        'received_at']


class OutgoingTextMessageAdmin(TextMessageAdmin):

    list_display = ['pk', 'from_phone', 'to_phone', 'message_text',
        'send_scheduled_at', 'sent_at']

    readonly_fields = ['from_phone', 'to_phone', 'message_text',
        'send_scheduled_at', 'sent_at']


admin.site.register(models.Experiment, ExperimentAdmin)

admin.site.register(models.Backend, BackendAdmin)

admin.site.register(models.Participant, ParticipantAdmin)

admin.site.register(models.IncomingTextMessage, IncomingTextMessageAdmin)

admin.site.register(models.OutgoingTextMessage, OutgoingTextMessageAdmin)
