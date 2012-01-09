# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

import StringIO


class UrllibSimulator(object):
    """
    Mocks up urllib2 so we can run tests without actually making HTTP
    requests to your API provider.
    """

    def __init__(self):
        self.requests_generated = 0
        self.urlopen_exception = None

    def Request(self, url, post_data=None, header_dict=None):
        """
        Sneaky! Looks like a class, but isn't one.
        """
        self.url = url
        self.post_data = post_data
        self.header_dict = header_dict
        self.requests_generated += 1
        return self.requests_generated

    def urlopen(self, *args, **kwargs):
        if self.urlopen_exception is not None:
            raise self.urlopen_exception
        return StringIO.StringIO("test")

    def set_urlopen_exception(self, exc):
        self.urlopen_exception = exc
