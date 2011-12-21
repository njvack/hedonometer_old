# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.db import models

import json

from texter.models import PhoneNumber, PhoneNumberField, AbstractBackend


class TropoBackend(AbstractBackend):
    """
    As the name suggests, a backend for handling communication with the
    Tropo SMS gateway.
    """

    sms_token = models.CharField(
        max_length=255)

    session_request_url = models.URLField(
        max_length=255,
        verify_exists=False,
        default='https://api.tropo.com/1.0/sessions')

    phone_number = PhoneNumberField(
        max_length=255)

    @property
    def name(self):
        return "Tropo: %s" % (self.phone_number)

    def handle_request(self, request):
        return []


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

        self.method = self.call_to.get('channel') or 'POST'

        self.text_content = s.get('initialText')
