# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.db import models

from texter.models import PhoneNumberField, AbstractBackend, Backend


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
