# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from celery.decorators import task
import models


@task
def schedule_task_day_start(pk, dt):
    td = models.TaskDay.objects.get(pk=pk)
    return td.start_day(dt)
