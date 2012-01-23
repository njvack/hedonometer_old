# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.test import TestCase

from . import models
from . import mocks


class TestIncomingMessage(TestCase):

    def setUp(self):
        self.itm = models.IncomingTextMessage()

    def testSkeleton(self):
        self.assertIsNotNone(self.itm)


class TestOutgoingTextMessage(TestCase):

    def setUp(self):
        self.exp = models.Experiment.objects.create(
            name='Test')
        self.in_phone = models.PhoneNumber('6085551212')
        self.out_phone = models.PhoneNumber('6085551213')
        self.txt = 'This is test'
        self.otm = self.exp.outgoingtextmessage_set.create(
            message_text=self.txt,
            from_phone=self.in_phone,
            to_phone=self.out_phone)
        self.ts1 = datetime.datetime(2011, 01, 14, 8, 31)

    def testGetMessageSetSent(self):
        self.otm.get_message_set_sent(self.ts1)
        self.assertEqual(self.ts1, self.otm.sent_at)


class TestDummyBackend(TestCase):

    def setUp(self):
        self.dbe = models.DummyBackend.objects.create()

    def testBackendAutomaticallyCreated(self):
        self.assertIsNotNone(self.dbe.backend)
        self.assertIsNotNone(self.dbe.backend.pk)

    def testBackendLinksToDummy(self):
        b = self.dbe.backend
        self.assertEqual(self.dbe, b.delegate_instance)

    def testHandleRequestDelegates(self):
        b = self.dbe.backend
        b.handle_request(None, None)
        dbe_reinit = models.DummyBackend.objects.get(pk=self.dbe.pk)
        self.assertEqual(1, dbe_reinit.handle_request_calls)

    def testSendMessageDelegates(self):
        b = self.dbe.backend
        b.send_message(None)
        dbe_reinit = models.DummyBackend.objects.get(pk=self.dbe.pk)
        self.assertEqual(1, dbe_reinit.send_message_calls)
