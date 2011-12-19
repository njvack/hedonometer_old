# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from texter.models import Backend
from . import models
from . import mocks


class TropoBackendTest(TestCase):

    def setUp(self):
        self.tb = models.TropoBackend.objects.create(
            sms_token='TEST',
            phone_number='6085551212')

    def testCreatesBackend(self):
        self.assertEqual(1, Backend.objects.count())

    def testDelegateInstanceFindsObject(self):
        b = Backend.objects.all()[0]
        self.assertEqual(self.tb, b.delegate_instance)
    
    def testBackendFindsName(self):
        b = Backend.objects.all()[0]
        self.assertEqual(self.tb.name, b.name)
        
    def testHandleMessageSessionReturnsEmptyList(self):
        messages = self.tb.handle_request(mocks.incoming_session_request())
        self.assertEqual(0, len(messages))
