# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.db import models
import re
import random


class PhoneNumber(object):

    description = "A 10-digit US telephone number"

    def __init__(self, number_string):
        self.original_string = number_string
        ns = re.sub("\D", "", number_string)
        ns = re.sub("^1", "", ns)
        self.cleaned = ns

    def __unicode__(self):
        n = self.cleaned
        if len(n) == 10:
            return self.ten_digit
        return n

    @property
    def ten_digit(self):
        n = self.cleaned
        return "(%s) %s-%s" % (n[0:3], n[3:6], n[6:])

    def __len__(self):
        return len(self.cleaned)

    def __str__(self):
        return self.__unicode__()

    def __eq__(self, other):
        sstr = str(self)
        ostr = str(other)
        return (sstr == ostr) and (len(sstr) > 0) and other is not None

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "%s.%s('%s')" % (
            self.__class__.__module__,
            self.__class__.__name__,
            str(self))


class PhoneNumberField(models.CharField):

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, PhoneNumber):
            return value

        return PhoneNumber(str(value))

    def get_prep_value(self, value):
        return value.cleaned

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^texter\.models\.PhoneNumberField"])


class StampedModel(models.Model):
    """
    All of our instances shall have a created_at and updated_at timestamp.
    """
    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    class Meta:
        abstract = True


def random_slug(slug_len):
    valid_chars='bcdfghjkmnpqrstvz'

    def fx():
        vcl = len(valid_chars)
        charnums = range(slug_len)
        slug = ''.join([random.choice(valid_chars) for cn in range(slug_len)])
        return slug
    return fx


class Experiment(StampedModel):

    name = models.CharField(
        max_length=100)

    url_slug = models.SlugField(
        unique=True,
        max_length=10,
        editable=False,
        default=random_slug(10))

    backend = models.ForeignKey('Backend',
        blank=True,
        null=True)


class TextMessage(StampedModel):
    """
    The base class for incoming and outgoing messages.
    """

    experiment = models.ForeignKey('Experiment')

    from_phone = PhoneNumberField(
        max_length=255)

    to_phone = PhoneNumberField(
        max_length=255)

    message_text = models.CharField(
        max_length=160,
        blank=True)

    sent_at = models.DateTimeField(
        blank=True,
        null=True)

    class Meta:
        abstract = True


class IncomingTextMessage(TextMessage):
    """
    Represents incoming text messages. Just like an abstract TextMessage,
    except that we know when we recieved it. In effect, this will probably
    always be the same as created_at. Some backends may not be able to
    distinguish between sent_at and received_at.
    """

    received_at = models.DateTimeField()


class OutgoingTextMessage(TextMessage):
    """
    Represents an outgoing text message. Similar to the abstract TextMessage,
    except we have a time at which the message is scheduled for delivery.
    """

    send_scheduled_at = models.DateTimeField(
        blank=True,
        null=True)


class MessageSendError(Exception):
    """
    A message send error that probably means "try again to deliver this
    message."
    """

    def __init__(self, reason, *args, **kwargs):
        self.reason = reason
        super(MessageSendError, self).__init__(*args, **kwargs)


class Backend(StampedModel):
    """
    A general, skeletal class for text backends. Doesn't actually implement
    much of anything, but uses a slightly odd style of polymorphism
    to delegate to actual implementing classes. Implementors must create
    a Backend instance when saved, and Experiments will be associated with
    Backends. Backend implementations will generally subclass AbstractBackend,
    which will take of the Backend-management for you.

    To be concrete, if you want an experiemnt to ues Tropo for messaging:
    * Create a TropoBackend.
    * Behind the scenes, it'll create a Backend
    * Set the Experiment's backend to the recently-created Backend.

    The methods you'll call on a Backend will be handle_request()
    and send_message().
    """

    delegate_classname = models.CharField(
        max_length=200,
        editable=False)

    delegate_pk = models.IntegerField(
        editable=False)

    name = models.CharField(
        max_length=200,
        editable=False)

    def __unicode__(self):
        return unicode(str(self))

    def __str__(self):
        return "Backend %s: %s" % (self.pk, self.name)

    @property
    def experiment(self):
        return self.experiment_set.all()[0]

    @property
    def delegate_instance(self):
        klass_parts = self.delegate_classname.split('.')
        module_name = '.'.join(klass_parts[:-1])
        m = __import__(module_name)
        for p in klass_parts[1:]:
            m = getattr(m, p)
        # Now we have a reference to our class...
        return m.objects.get(pk=self.delegate_pk)

    def handle_request(self, request):
        return self.delegate_instance.handle_request(request)

    def send_message(self, message):
        return self.delegate_instance.send_message(request)


class AbstractBackend(StampedModel):
    """
    For convenience, backend implementation should inherit from this.
    Implementors must implement handle_request(), send_message(),
    and override save() to create an instance of Backend.
    """

    class Meta:
        abstract = True

    @property
    def backend(self):
        return Backend.objects.get(
            delegate_classname=self.qualified_classname,
            delegate_pk=self.pk)

    @property
    def experiment(self):
        return self.backend.experiment

    def handle_request(self, request):
        """
        Handle an incoming request -- be it a text message notification
        or a request for a message.

        Return a list of messages.
        """
        raise NotImplementedError()

    def send_message(self, message):
        raise NotImplementedError()

    @property
    def qualified_classname(self):
        return self.__module__+'.'+self.__class__.__name__

    def save(self, *args, **kwargs):
        creating = False
        if self.pk is None:
            creating = True

        super(AbstractBackend, self).save(*args, **kwargs)

        if creating:
            Backend.objects.create(
                delegate_classname=self.qualified_classname,
                delegate_pk=self.pk,
                name=self.name)
        else:
            b = self.backend()
            b.name = self.name
            b.save()
