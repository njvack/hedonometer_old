# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import datetime

import logging
logger = logging.getLogger('texter')

import models


def incoming(request, url_slug):
    exp = get_object_or_404(models.Experiment, url_slug=url_slug)
    backend = exp.backend
    response = HttpResponse()
    messages = backend.handle_request(request, response)
    for msg in messages:
        try:
            exp.handle_incoming_message(msg)
        except models.UnknownPhoneNumberError:
            exp.create_and_send_message(
                msg.from_phone,
                exp.unknown_participant_message,
                datetime.datetime.now())
        except models.NoPendingSampleError:
            exp.create_and_send_message(
                msg.from_phone,
                exp.no_response_needed_message,
                datetime.datetime.now())
        except models.MessageParseError:
            exp.create_and_send_message(
                msg.from_phone,
                exp.bad_answer_message,
                datetime.datetime.now())

    return response
