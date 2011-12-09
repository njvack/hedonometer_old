from django.db import models
import re


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


class Experiment(StampedModel):

    name = models.CharField(
        max_length=100)

    url_slug = models.SlugField(
        max_length=10,
        editable=False)


class Backend(StampedModel):
    """
    A general, skeletal class for text backends. Doesn't actually implement
    much of anything, but uses a slightly odd style of polymorphism
    to delegate to actual implementing classes. Implementors must create
    a Backend instance when saved, and Experiments will be associated with
    Backends.

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

    delegate_pk = models.IntegerField()

    name = models.CharField(
        max_length=200,
        editable=False)


class AbstractBackend(StampedModel):
    """
    For convenience, backend implementation should inherit from this.
    Implementors must implement handle_request(), send_message(),
    and override save() to create an instance of Backend.
    """

    class Meta:
        abstract = True

    def handle_request(self, request):
        """
        Handle an incoming request -- be it a text message notification
        or a request for a message.

        Return a list of messages.
        """
        raise NotImplementedError()

    def send_message(self, message):
        raise NotImplementedError()


class TropoBackend(AbstractBackend):
    """
    As the name suggests, a backend for handling communication with the
    Tropo SMS gateway.
    """

    sms_token = models.CharField(
        max_length=255)

    session_request_url = models.URLField(
        max_length=255,
        verify_exists=False,
        default='https://api.tropo.com/1.0/sessions')

    phone_number = PhoneNumberField(
        max_length=255)

    @property
    def _name(self):
        return "Tropo: %s" % (self.phone_number)

    def save(self, *args, **kwargs):
        creating = False
        if self.pk is None:
            creating = True

        super(TropoBackend, self).save(*args, **kwargs)

        if creating:
            Backend.objects.create(
                delegate_classname=self.__class__.__name__,
                delegate_pk=self.pk,
                name=self._name)
        else:
            b = Backend.objects.get(
                delegate_classname=self.__class__.__name__,
                delegate_pk=self.pk)
            b.name = self._name
            b.save()
