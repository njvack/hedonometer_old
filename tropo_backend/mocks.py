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


class Tropo(object):

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


class HttpRequest(object):

    def __init__(self, post_data):
        self.method = 'POST'
        self.raw_post_data = post_data


INCOMING_SMS_JSON = r"""{
"session": {
    "from": {
        "network": "SMS",
        "id": "16084486677",
        "channel": "TEXT",
        "name": null
    },
    "to": {
        "network": "SMS",
        "id": "16086164697",
        "channel": "TEXT",
        "name": null
    },
    "timestamp": "2011-07-25T18:01:28.926Z",
    "initialText": "One more",
    "headers": {
        "Content-Length": "124",
        "Via": "SIP/2.0/UDP 10.6.93.101:5066;branch=z9hG4bKcc4dhy",
        "From": "<sip:689C26C0-0EEA-4640-A830B7A21BF03950@10.6.61.201;channel=private;user=16084486677;msg=One%20more;network=SMS;step=2>;tag=t1m87o",
        "To": "<sip:9996127024@10.6.69.204:5061;to=16086164697>",
        "Contact": "<sip:10.6.93.101:5066;transport=udp>",
        "CSeq": "1 INVITE",
        "Call-ID": "w0leo4",
        "Max-Forwards": "70",
        "Content-Type": "application/sdp"
    },
    "userType": "HUMAN",
    "callId": "1b5d038d090d913b1856d77a2a06cd85",
    "id": "8fe3744201a2600b844751853db86933",
    "accountId": "62371"
}
}"""


def incoming_sms_request():
    return HttpRequest(INCOMING_SMS_JSON)


INCOMING_SESSION_JSON = r"""{
"session": {
    "parameters": {
        "path": "/test/",
        "format": "json",
        "pk": "1"
    },
    "timestamp": "2011-07-27T21:31:21.724Z",
    "initialText": null,
    "userType": "NONE",
    "callId": null,
    "id": "5aa1039bb972f8f8e9d5beaf5cc70262",
    "accountId": "62371"
}
}"""


def incoming_session_request():
    return HttpRequest(INCOMING_SESSION_JSON)
