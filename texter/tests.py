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
from django.db import IntegrityError

from . import models
from . import mocks

EARLY_TODAY = datetime.datetime(2011, 1, 24, 8, 59)
START_TODAY = datetime.datetime(2011, 1, 24, 9, 0)
MID_TODAY = datetime.datetime(2011, 1, 24, 13, 15)
END_TODAY = datetime.datetime(2011, 1, 24, 19, 0)
LATE_TODAY = datetime.datetime(2011, 1, 24, 19, 1)
DATE_TODAY = EARLY_TODAY.date()
TIME_EARLY = EARLY_TODAY.time()
TIME_START = START_TODAY.time()
TIME_MID = MID_TODAY.time()
TIME_END = END_TODAY.time()


class TestExperiment(TestCase):

    def setUp(self):
        self.exp = models.Experiment.objects.create(
            name='Test')

        def testNothing(self):
            pass # We'll just make sure the experiment gets created


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
        self.otm.get_message_mark_sent(self.ts1)
        self.assertEqual(self.ts1, self.otm.sent_at)


class TestTaskDay(TestCase):

    def setUp(self):
        self.exp = models.Experiment.objects.create(
            name='Test')
        self.ppt = self.exp.participant_set.create(
            phone_number=models.PhoneNumber('6085551212'),
            stopped=False,
            id_code='test',
            start_date=DATE_TODAY)
        self.td = self.ppt.taskday_set.create(
            task_date=DATE_TODAY,
            start_time=TIME_START,
            end_time=TIME_END)

    def testTaskDaySetsFirstAndLastContact(self):
        self.assertEqual(START_TODAY, self.td.earliest_contact)
        self.assertEqual(END_TODAY, self.td.latest_contact)

    def testTaskDayEligibleToRun(self):
        self.assertTrue(self.td.eligible_to_start_at(MID_TODAY))
        self.assertFalse(self.td.eligible_to_start_at(EARLY_TODAY))
        self.assertFalse(self.td.eligible_to_start_at(LATE_TODAY))
        self.td.set_run_state('running')
        self.assertFalse(self.td.eligible_to_start_at(MID_TODAY))


class TestParticipant(TestCase):

    def setUp(self):
        self.exp = models.Experiment.objects.create(
            name='Test')
        self.ppt = self.exp.participant_set.create(
            phone_number=models.PhoneNumber('6085551212'),
            stopped=False,
            id_code='test',
            start_date=DATE_TODAY)

    def testDuplicatesNotAllowed(self):
        with self.assertRaises(IntegrityError):
            ppt2 = self.exp.participant_set.create(
                phone_number=models.PhoneNumber('6085551212'),
                stopped=False,
                id_code='test2',
                start_date=DATE_TODAY)


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
