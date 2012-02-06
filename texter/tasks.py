# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from celery.decorators import task
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
    return ss.schedule_question_parts(dt)


@task
def send_message_to_participant(participant_id, message_text, dt):
    ppt = models.Participant.objects.get(pk=participant_id)
    exp = ppt.experiment
    otm = exp.build_outgoing_message(
        ppt.phone_number,
        message_text,
        dt)
    exp.send_outgoing_message(otm)
    return otm
