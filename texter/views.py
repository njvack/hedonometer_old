# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import datetime
import csv

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
            logger.debug("UnknownPhoneNumberError")
            exp.create_and_send_message(
                msg.from_phone,
                exp.unknown_participant_message,
                datetime.datetime.now())
        except models.NoPendingSampleError:
            logger.debug("NoPendingSampleError")
            exp.create_and_send_message(
                msg.from_phone,
                exp.no_response_needed_message,
                datetime.datetime.now())
        except models.MessageParseError:
            logger.debug("MessageParseError")
            exp.create_and_send_message(
                msg.from_phone,
                exp.bad_answer_message,
                datetime.datetime.now())

    return response


def samples_csv(request, url_slug):
    exp = get_object_or_404(models.Experiment, url_slug=url_slug)
    response = HttpResponse(content_type='text/plain')
    writer = csv.writer(response)
    participants = exp.participant_set.order_by('id')
    columns = [
        'participant_id', 'participant_code', 'sample_id', 'status',
        'sent_at', 'answered_at', 'answer']

    writer.writerow(columns)
    for p in participants:
        samples = p.get_reportable_samples()
        for s in samples:
            answer = ''
            if s.answered_by is not None:
                answer = s.answered_by.message_text
            data = [p.pk, p.id_code, s.pk, s.run_state,
                _time_format(s.sent_at), _time_format(s.answered_at), answer]
            writer.writerow(data)

    return response


def outgoing_texts_csv(request, url_slug):
    exp = get_object_or_404(models.Experiment, url_slug=url_slug)
    response = HttpResponse(content_type='text/plain')
    writer = csv.writer(response)
    participants = {}
    missing = models.Participant(pk='Unknown', id_code='Unknown')

    columns = [
        'participant_id', 'participant_code', 'text_message_id',
        'sent_at', 'message_text']

    writer.writerow(columns)
    messages = exp.outgoingtextmessage_set.all()
    for m in messages:
        key = str(m.to_phone)
        if key not in participants:
            try:
                participants[key] = exp.participant_set.get(
                    phone_number=m.to_phone)
            except models.Participant.DoesNotExist:
                participants[key] = missing
        p = participants[key]
        data = [p.pk, p.id_code, m.pk, _time_format(m.sent_at), m.message_text]
        writer.writerow(data)
    return response


def incoming_texts_csv(request, url_slug):
    exp = get_object_or_404(models.Experiment, url_slug=url_slug)
    response = HttpResponse(content_type='text/plain')
    writer = csv.writer(response)
    participants = {}
    missing = models.Participant(pk='Unknown', id_code='Unknown')

    columns = [
        'participant_id', 'participant_code', 'text_message_id',
        'received_at', 'message_text']

    writer.writerow(columns)
    messages = exp.incomingtextmessage_set.all()
    for m in messages:
        key = str(m.from_phone)
        if key not in participants:
            try:
                participants[key] = exp.participant_set.get(
                    phone_number=m.from_phone)
            except models.Participant.DoesNotExist:
                participants[key] = missing
        p = participants[key]
        data = [p.pk, p.id_code, m.pk, _time_format(m.received_at),
            m.message_text]
        writer.writerow(data)
    return response


def _time_format(dt):
    if dt is not None:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return ''
