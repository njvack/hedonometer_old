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

from . import models


class TestIncomingMessage(TestCase):

    def setUp(self):
        self.itm = models.IncomingTextMessage()

    def testSkeleton(self):
        self.assertIsNotNone(self.itm)


class TestOutgoingTextMessage(TestCase):

    def setUp(self):
        self.otm = models.OutgoingTextMessage()

    def testSkeleton(self):
        self.assertIsNotNone(self.otm)
