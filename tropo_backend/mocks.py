# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

import logging
logger = logging.getLogger("tropo_backend")
from . import models


class OutgoingTropoSession(object):

    def __init__(self, *args, **kwargs):
        self.request_count = 0

    def request_session(self, options):
        self.request_count += 1
        logger.debug(
            "%s call: mocks.OutgoingTropoSession#request_session: %s" %
            (self.request_count, options))


class Tropo(models.TextingTropo):

    def __init__(self, *arg, **kwargs):
        self.called = ''
        self.things_said = 0
        self.things_said_list = []
        self.hangups = 0

    def call(self, number, *args, **kwargs):
        self.called = number

    def say(self, message):
        self.things_said += 1
        self.things_said_list.append(message)

    def hangup(self):
        self.hangups += 1

    def RenderJson(self):
        return '{}'
