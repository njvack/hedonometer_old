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
import urllib2
import json

from texter.models import (
    Backend, IncomingTextMessage, OutgoingTextMessage, Experiment,
    MessageSendError)
from . import models
from . import mocks


class TropoBackendTest(TestCase):

    def setUp(self):
        self.mock_http_client = mocks.UrllibSimulator()

        self.tb = models.TropoBackend.objects.create(
            sms_token='TEST',
            phone_number='6085551212',
            http_library=self.mock_http_client)

        self.experiment = Experiment.objects.create(
            name='Test',
            url_slug='test',
            backend=self.tb.backend)

        self.ogm = self.experiment.outgoingtextmessage_set.create(
            from_phone='6085551212',
            to_phone='6085551213',
            message_text='test')

        self.response = mocks.HttpResponse()

    def testCreatesBackend(self):
        self.assertEqual(1, Backend.objects.count())

    def testExperimentAssociation(self):
        self.assertEqual(self.experiment, self.tb.backend.experiment)
        self.assertEqual(self.experiment, self.tb.experiment)

    def testDelegateInstanceFindsObject(self):
        b = Backend.objects.all()[0]
        self.assertEqual(self.tb, b.delegate_instance)

    def testBackendFindsName(self):
        b = Backend.objects.all()[0]
        self.assertEqual(self.tb.name, b.name)

    def testHandleRequestForSessionReturnsEmptyList(self):
        messages = self.tb.handle_request(
            mocks.incoming_session_request(),
            self.response)
        self.assertEqual(0, len(messages))

    def testHandleRequestForIncomingModifiesRequest(self):
        req = mocks.incoming_session_request({
            'pk': str(self.ogm.pk)})

        messages = self.tb.handle_request(
            mocks.incoming_session_request(),
            self.response)
        self.assertEqual(1, self.response.writes)

    def testHandleRequestForIncomingWritesJson(self):
        req = mocks.incoming_session_request({
            'pk': str(self.ogm.pk)})

        messages = self.tb.handle_request(req, self.response)
        self.assertEqual('application/json', self.response['Content-Type'])
        parsed = json.loads(str(self.response))

    def testHandleRequestForIncomingMarksSent(self):
        req = mocks.incoming_session_request({
            'pk': str(self.ogm.pk)})

        messages = self.tb.handle_request(req, self.response)
        ogm = self.experiment.outgoingtextmessage_set.get(pk=self.ogm.pk)
        self.assertIsNotNone(ogm.sent_at)

    def testHandleRequestIncomingRaisesWithNotFoundPk(self):
        req = mocks.incoming_session_request({
            'pk': '100'})

        with self.assertRaises(OutgoingTextMessage.DoesNotExist):
            messages = self.tb.handle_request(req, self.response)

    def testHandleRequestIncomingRaisesWithInvalidPk(self):
        req = mocks.incoming_session_request({
            'pk': 'a'})

        with self.assertRaises(ValueError):
            messages = self.tb.handle_request(req, self.response)

    def testHandleRequestForSMSReturnsMessage(self):
        messages = self.tb.handle_request(
            mocks.incoming_sms_request(),
            self.response)
        self.assertEqual(1, len(messages))
        self.assertIsInstance(messages[0], IncomingTextMessage)
        self.assertIsNotNone(messages[0].pk)

    def testSendMessageReturnsTrueWithSavedMessage(self):
        self.assertTrue(self.tb.send_message(self.ogm))

    def testSendMessageGeneratesHttpRequest(self):
        self.tb.send_message(self.ogm)
        self.assertEqual(1, self.mock_http_client.requests_generated)

    def testSendMessageHandlesIOErrors(self):
        self.mock_http_client.set_urlopen_exception(
            urllib2.URLError("Test error"))
        with self.assertRaises(MessageSendError):
            self.tb.send_message(self.ogm)


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


class OutgoingSessionTest(TestCase):

    def setUp(self):
        self.mock_http_client = mocks.UrllibSimulator()

        self.tb = models.TropoBackend.objects.create(
            sms_token='TEST',
            phone_number='6085551212',
            http_library=self.mock_http_client)

        self.experiment = Experiment.objects.create(
            name='OutgoingSessionTest',
            url_slug='test',
            backend=self.tb.backend)

        self.sess = self.tb.make_outgoing_session()

        self.ogm = self.experiment.outgoingtextmessage_set.create(
            from_phone='6085551212',
            to_phone='6085551213',
            message_text='test')

    def testRequestSessionReturnsTrue(self):
        self.assertTrue(self.sess.request_session(self.ogm))

    def testRequestSessionRaisesWithNone(self):
        with self.assertRaises(TypeError):
            self.sess.request_session(None)

    def testRequestSessionRaisesWithUnsavedMessage(self):
        with self.assertRaises(ValueError):
            self.sess.request_session(OutgoingTextMessage())

    def testRequestSessionGeneratesHttpRequest(self):
        self.sess.request_session(self.ogm)
        self.assertEqual(1, self.mock_http_client.requests_generated)

    def testRequestSessionCanRaiseUrlError(self):
        exc = urllib2.URLError("Test error")
        self.mock_http_client.set_urlopen_exception(exc)
        with self.assertRaises(urllib2.URLError):
            self.sess.request_session(self.ogm)
