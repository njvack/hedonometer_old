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

import datetime

from texter.models import Backend, IncomingTextMessage, Experiment
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

    def testHandleMessageForSessionReturnsEmptyList(self):
        messages = self.tb.handle_request(mocks.incoming_session_request())
        self.assertEqual(0, len(messages))


class TropoRequestTest(TestCase):

    def setUp(self):
        self.session_req = models.TropoRequest(mocks.INCOMING_SESSION_JSON)
        self.sms_req = models.TropoRequest(mocks.INCOMING_SMS_JSON)

    def testIsIncoming(self):
        self.assertTrue(self.sms_req.is_incoming)
        self.assertFalse(self.session_req.is_incoming)

    def testParameters(self):
        self.assertEqual({}, self.sms_req.REQUEST)
        self.assertIn('path', self.session_req.REQUEST)

    def testMethod(self):
        self.assertEqual('POST', self.session_req.method)
        self.assertEqual('TEXT', self.sms_req.method)

    def testCallTo(self):
        self.assertEqual({}, self.session_req.call_to)
        self.assertIn('id', self.sms_req.call_to)
        self.assertIn('phone_number', self.sms_req.call_to)

    def testCallFrom(self):
        self.assertEqual({}, self.session_req.call_from)
        self.assertIn('id', self.sms_req.call_from)
        self.assertIn('phone_number', self.sms_req.call_from)

    def testInitialText(self):
        self.assertIsNone(self.session_req.text_content)
        self.assertIsNotNone(self.sms_req.text_content)

    def testTimestamp(self):
        # 2011-07-25T18:01:28.926Z in the mock request
        dt = datetime.datetime(2011, 7, 25, 18, 1, 28, 926000)
        self.assertEqual(dt, self.sms_req.timestamp)
