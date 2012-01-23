# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.http import HttpResponse
from django.shortcuts import get_object_or_404


import logging
logger = logging.getLogger('texter')

import models

def incoming(request, url_slug):
    exp = get_object_or_404(models.Experiment, url_slug=url_slug)
    backend = exp.backend
    response = HttpResponse()
    backend.handle_request(request, response)
    return response
