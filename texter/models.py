# coding: utf8
# Part of hedonometer -- a text-messing-based experience sampler
#
# Copyright (c) 2011 Board of Regents of the University of Wisconsin System

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


from dirtyfields import DirtyFieldsMixin

import re
import random
import datetime
from collections import defaultdict

import logging
logger = logging.getLogger('texter')


PART_SAMPLE_DELAY_SEC = 3


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

    experiment_length_days = models.IntegerField(
        "Total task days",
        default=1)

    max_samples_per_day = models.IntegerField(
        default=1)

    min_time_between_samples = models.IntegerField(
        help_text="(Seconds)",
        default=3600)

    max_time_between_samples = models.IntegerField(
        help_text="(Seconds)",
        default=5400)

    accepted_answer_pattern = models.CharField(
        help_text="(Regular expression)",
        max_length=255,
        default=".*")

    answer_ignores_case = models.BooleanField(
        default=True)

    backend = models.ForeignKey('Backend',
        blank=True,
        null=True)

    def __unicode__(self):
        return unicode(str(self))

    def __str__(self):
        if self.backend is None:
            backend_str = "No backend"
        else:
            backend_str = str(self.backend)

        return "Experiment %s: %s (%s, %s)" % (
            self.pk, self.url_slug, self.name, backend_str)


class QuestionPart(StampedModel):

    experiment = models.ForeignKey('Experiment')

    message_text = models.CharField(
        max_length=160)

    order = models.IntegerField(default=1)


class ScheduledSample(DirtyFieldsMixin, StampedModel):

    task_day = models.ForeignKey('TaskDay')

    scheduled_at = models.DateTimeField()

    sent_at = models.DateTimeField(
        blank=True,
        null=True)

    answered_at = models.DateTimeField(
        blank=True,
        null=True)

    run_state = models.CharField(
        max_length=255,
        default='scheduled')

    def __init__(self, *args, **kwargs):
        self.changed_fields = {}
        self.skip_scheduling = kwargs.pop('skip_scheduling', False)
        super(ScheduledSample, self).__init__(*args, **kwargs)

    @property
    def experiment(self):
        return self.task_day.experiment

    def set_run_state(self, new_state, save=True):
        logger.debug("%s -> %s" % (self, new_state))
        self.run_state = new_state
        if save:
            self.save()

    def is_scheduled(self):
        return self.run_state == 'scheduled'

    def schedule_send(self):
        logger.debug("Scheduling %s at %s" % (self, self.scheduled_at))
        result = None
        if not self.skip_scheduling:
            result = tasks.send_scheduled_sample(self.pk, self.scheduled_at)
        return result

    def schedule_question_parts(self, dt, save=True):
        if not self.is_scheduled():
            return False
        self.sent_at = dt
        self.set_run_state('sent', save)
        return True

    def mark_answered(self, dt, save=True):
        if not self.is_sent():
            return False
        self.answered_at = dt
        self.sent_run_state = 'answered'
        if save:
            self.save()
        return True

    def is_sent(self):
        return self.run_state == 'sent'

    def has_been_sent(self):
        return self.run_state == 'sent' or self.run_state == 'answered'

    def __str__(self):
        return "ScheduledSample %s: %s" % (self.pk, self.run_state)

    def save(self, *args, **kwargs):
        self.changed_fields = self.get_dirty_fields()
        super(ScheduledSample, self).save(*args, **kwargs)


@receiver(post_save, sender=ScheduledSample)
def scheduled_sample_post_save(sender, instance, created, **kwargs):
    ss = instance
    if created or 'scheduled_at' in ss.changed_fields:
        ss.schedule_send()


class Participant(StampedModel):

    experiment = models.ForeignKey('Experiment')

    phone_number = PhoneNumberField(
        max_length=255)

    stopped = models.BooleanField(
        default=False)

    start_date = models.DateField()

    normal_earliest_message_time = models.TimeField(
        default="9:00")

    normal_latest_message_time = models.TimeField(
        default="21:00")

    id_code = models.CharField(
        max_length=255,
        blank=True,
        null=True)

    class Meta:
        unique_together = ['experiment', 'phone_number']

    def __unicode__(self):
        return unicode(str(self))

    def __str__(self):
        return "Participant %s: %s - %s" % (
            self.pk, self.phone_number, self.id_code)


class TaskDay(DirtyFieldsMixin, StampedModel):
    """
    A day for a participant. Stores a date, start and end times, and a
    run_state.
    When saved, we schedule a start event; this event should check and see
    if we're actually 'waiting' and then start us.
    """

    participant = models.ForeignKey('Participant')

    task_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    earliest_contact = models.DateTimeField(
        editable=False)

    latest_contact = models.DateTimeField(
        editable=False)

    _run_state = models.CharField(
        max_length=255,
        default="waiting",
        editable=False)

    def __init__(self, *args, **kwargs):
        self.schedules = defaultdict(list)
        self.force_reschedule = False
        self.skip_scheduling_samples = kwargs.pop(
            'skip_scheduling_samples', False)
        super(TaskDay, self).__init__(*args, **kwargs)

    def sample_count_to_schedule(self):
        asked_and_scheduled_count = (
            self.scheduled_samples().count() + self.asked_samples().count())
        max_count = self.participant.experiment.max_samples_per_day
        return max_count - asked_and_scheduled_count

    def next_sample_time(self):
        scheds = self.scheduled_samples()
        outstandings = self.asked_and_scheduled_samples()
        next_sample_base = max(
            [s.scheduled_at for s in outstandings] + [self.earliest_contact])
        sec = 0
        if outstandings.count() == 0:
            sec = random.randint(0, self.min_time_between_samples)
        else:
            sec = random.randint(
                self.min_time_between_samples, self.max_time_between_samples)
        delta = datetime.timedelta(seconds=sec)
        next_time = next_sample_base + delta
        if next_time > self.latest_contact:
            return None
        else:
            return next_time

    def scheduled_samples(self):
        return self.scheduledsample_set.filter(run_state='scheduled')

    def rescheduled_samples(self):
        return self.scheduledsample_set.filter(run_state='rescheduled')

    def asked_samples(self):
        return self.scheduledsample_set.filter(
            run_state__in=['sent', 'answered'])

    def asked_and_scheduled_samples(self):
        return self.scheduledsample_set.filter(
            run_state__in=['scheduled', 'sent', 'answered'])

    @property
    def min_time_between_samples(self):
        return self.experiment.min_time_between_samples

    @property
    def max_time_between_samples(self):
        return self.experiment.max_time_between_samples

    @property
    def experiment(self):
        return self.participant.experiment

    def is_waiting(self):
        return self._run_state == 'waiting'

    def is_running(self):
        return self._run_state == 'running'

    def eligible_to_start_at(self, dt):
        return (
            (self.is_waiting()) and
            (dt >= self.earliest_contact) and
            (dt < self.latest_contact))

    def eligible_to_end_at(self, dt):
        return (
            self.is_running() and
            dt >= self.latest_contact)

    def start_day(self, dt, save=True):
        if not self.eligible_to_start_at(dt):
            logger.debug("%s not eligible to start at %s" % (self, dt))
            return False

        self.set_run_state('running', save)
        return True

    def end_day(self, dt, save=True):
        if not self.eligible_to_end_at(dt):
            logger.debug("%s not eligible to end at %s" % (self, dt))
            return False
        self.set_run_state('completed', save)
        return True

    def schedule_start_day(self, dt):
        result = tasks.start_task_day.apply_async(
            args=[self.pk, dt], eta=dt)
        self.schedules['start'].append(result)
        return result

    def schedule_end_day(self, dt):
        result = tasks.end_task_day.apply_async(
            args=[self.pk, dt], eta=dt)
        self.schedules['end'].append(result)
        return result

    def set_run_state(self, new_state, save=True):
        logger.debug("%s -> %s" % (self, new_state))
        self._run_state = new_state
        if save:
            self.save()

    def __set_contact_times(self):
        self.earliest_contact = datetime.datetime.combine(
            self.task_date, self.start_time)
        self.latest_contact = datetime.datetime.combine(
            self.task_date, self.end_time)

    def _reschedule_samples(self):
        sched = self.scheduled_samples()
        for samp in sched:
            samp.set_run_state('rescheduled')
        for snum in range(self.sample_count_to_schedule()):
            next_time = self.next_sample_time()
            if next_time is None:
                return
            ss = self.scheduledsample_set.create(
                scheduled_at=next_time,
                skip_scheduling=self.skip_scheduling_samples)

    def save(self, *args, **kwargs):
        self.__set_contact_times()
        self.changed_fields = self.get_dirty_fields()
        super(TaskDay, self).save(*args, **kwargs)


@receiver(post_save, sender=TaskDay)
def task_day_post_save(sender, instance, created, **kwargs):
    td = instance
    reschedule = td.force_reschedule
    if 'earliest_contact' in td.changed_fields:
        reschedule = True
        td.schedule_start_day(td.earliest_contact)
    if 'latest_contact' in td.changed_fields:
        reschedule = True
        td.schedule_end_day(td.earliest_contact)

    if reschedule:
        td._reschedule_samples()


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

    def get_message_mark_sent(self, dt, save=True):
        self.sent_at = dt
        if save:
            self.save()
        return self.message_text


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

    To be concrete, if you want an experiment to use Tropo for messaging:
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

    def handle_request(self, request, response):
        return self.delegate_instance.handle_request(request, response)

    def send_message(self, message):
        return self.delegate_instance.send_message(message)

# This is way down here to avoid circular import issues
import tasks


class AbstractBackend(StampedModel):
    """
    For convenience, backend implementation should inherit from this.
    Implementors must implement handle_request(), send_message(),
    and override save() to create an instance of Backend.
    """

    phone_number = PhoneNumberField(
        max_length=255)

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

    def handle_request(self, request, response):
        """
        Handle an incoming request -- be it a text message notification
        or a request for a message.

        Return a list IncomingTextMessages, which have been saved to the
        database. The list may be empty.

        May write to or otherwise modify response. Then again, may not.
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
            b = self.backend
            b.name = self.name
            b.save()


class DummyBackend(AbstractBackend):
    """
    As the name suggests, a dummy backend. It's used in testing, and for you
    to see what a do-nothing implementation of a Backend would look like.
    """

    handle_request_calls = models.IntegerField(default=0)

    send_message_calls = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        self.handle_request_calls = 0
        self.send_message_calls = 0

        super(DummyBackend, self).__init__(*args, **kwargs)

    @property
    def name(self):
        return "Dummy: %s handle calls, %s send calls" % (
            self.handle_request_calls, self.send_message_calls)

    def handle_request(self, request, response):
        self.handle_request_calls += 1
        self.save()

    def send_message(self, message):
        self.send_message_calls += 1
        self.save()
