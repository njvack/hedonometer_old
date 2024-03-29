# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from celery.decorators import task
import datetime
import models


@task
def start_task_day(pk, dt):
    td = models.TaskDay.objects.get(pk=pk)
    return td.start_day(dt)


@task
def end_task_day(pk, dt):
    td = models.TaskDay.objects.get(pk=pk)
    return td.end_day(dt)


@task
def send_scheduled_sample(pk, dt):
    ss = models.ScheduledSample.objects.get(pk=pk)
    actual_run_time = datetime.datetime.now()
    return ss.send_question_parts(
        actual_run_time, models.PART_SAMPLE_DELAY_SEC)


@task
def send_message_to_participant(participant_id, message_text, dt):
    ppt = models.Participant.objects.get(pk=participant_id)
    exp = ppt.experiment
    otm = exp.build_outgoing_message(
        ppt.phone_number,
        message_text,
        dt)
    otm.send()
    return otm


@task
def send_outgoing_message(pk):
    ogm = models.OutgoingTextMessage.objects.get(pk=pk)
    ogm.send()
