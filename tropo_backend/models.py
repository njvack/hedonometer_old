# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.db import models

import json
import datetime
import urllib2

import tropo

from texter.models import (PhoneNumber, PhoneNumberField, AbstractBackend,
    IncomingTextMessage, OutgoingTextMessage, MessageSendError)

import logging
logger = logging.getLogger(__name__)


class TropoBackend(AbstractBackend):
    """
    As the name suggests, a backend for handling communication with the
    Tropo SMS gateway.

    Does all comunication via the JSON API.
    """

    sms_token = models.CharField(
        max_length=255)

    session_request_url = models.URLField(
        max_length=255,
        verify_exists=False,
        default='https://api.tropo.com/1.0/sessions')

    phone_number = PhoneNumberField(
        max_length=255)

    def __init__(self, *args, **kwargs):
        self.http_library = kwargs.pop('http_library', urllib2)

        super(TropoBackend, self).__init__(*args, **kwargs)

    @property
    def name(self):
        key_short = self.sms_token[0:7]+"..."
        return "Tropo: %s, token: %s" % (self.phone_number, key_short)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return str(self)

    def handle_request(self, request, response):
        logger.debug("TropoBackend#handle_request: got %s" %
            (request.raw_post_data))
        tr = TropoRequest(request.raw_post_data)
        messages = None
        if tr.is_incoming:
            messages = self._handle_incoming(tr, response)
        else:
            messages = self._handle_session(tr, response)
        return messages

    def _handle_incoming(self, tr, response):
        logger.debug("TropoBackend#_handle_incoming()")
        messages = []
        itm = self.experiment.incomingtextmessage_set.create(
            from_phone=tr.call_from['phone_number'],
            to_phone=tr.call_to['phone_number'],
            message_text=tr.text_content,
            sent_at=tr.timestamp,
            received_at=datetime.datetime.now())
        messages.append(itm)
        return messages

    def _handle_session(self, tr, response):
        dt = datetime.datetime.now()
        response['Content-Type'] = 'application/json'
        ogm_pk = tr.parameters.get('pk')
        ogm = self.experiment.outgoingtextmessage_set.get(pk=ogm_pk)
        logger.debug("TropoBackend#_handle_session() found %s" % (repr(ogm)))
        t = tropo.Tropo()
        t.say(ogm.get_message_mark_sent(dt))
        t.hangup()
        response.write(t.RenderJson())
        return []

    def send_message(self, message):
        sess = self.make_outgoing_session()
        try:
            return sess.request_session(message)
        except IOError as e:
            raise MessageSendError(reason=e)

    def make_outgoing_session(self):
        return OutgoingSession(
            self.session_request_url,
            self.sms_token,
            self.http_library)


class TropoRequest(object):
    """
    Represents an incoming HTTP request from Tropo -- parses the JSON data,
    and generally tells us what we need in order to do something with it.
    This generates something that looks very superficially like a Django
    HttpRequest.
    """

    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.data = json.loads(self.raw_json)
        self._session = self.data.get('session') or {}
        self._parse_session(self._session)

    def _parse_session(self, s):
        self.is_incoming = ("to" in s)
        self.REQUEST = s.get("parameters") or {}
        self.POST = self.REQUEST

        self.call_to = s.get('to') or {}
        if 'id' in self.call_to:
            self.call_to['phone_number'] = PhoneNumber(self.call_to['id'])

        self.call_from = s.get('from') or {}
        if 'id' in self.call_from:
            self.call_from['phone_number'] = PhoneNumber(self.call_from['id'])

        self.timestamp = datetime.datetime.strptime(
            s['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

        self.method = self.call_to.get('channel') or 'POST'

        self.parameters = s.get('parameters')

        self.text_content = s.get('initialText')


class OutgoingSession(object):
    """
    Tropo's API works such that instead of saying "hey Tropo, send this
    message," you say "hey Tropo, here's some info about the message I want
    to send" and it makes an HTTP request back to your app with that info.

    This class handles the "hey Tropo, here's the some info about the message
    I want to send" part -- it makes HTTP requests to the Tropo API.

    These objects will alway be generated either by tests or a TropoBackend
    instance; hence the slightly awkward initialzation API.
    """

    def __init__(self, api_url, sms_token, http_library):
        """
        No surprises here. The http_library parameter will usually be
        urllib2 (set by a TropoBackend) but can be something that acts like
        it, for testing purposes.
        """
        self.api_url = api_url
        self.sms_token = sms_token
        self.http_library = http_library

    def request_session(self, outgoing_message):
        if not isinstance(outgoing_message, OutgoingTextMessage):
            raise TypeError("outgoing_message is not an instance of "+
                "OutgoingTextMessage")
        if outgoing_message.pk is None:
            raise ValueError("outgoing_message must be saved before sending")

        opts = {'token': self.sms_token, 'pk': str(outgoing_message.pk)}
        opts_json = json.dumps(opts)
        logger.debug("OutgoingSession making request to %s: %s" %
            (self.api_url, opts_json))
        req = self.http_library.Request(
            self.api_url,
            opts_json,
            {'content-type', 'application/json'})
        stream = self.http_library.urlopen(req)
        response = stream.read()
        logger.debug("OutgoingSession read: %s" % (response))
        return True
