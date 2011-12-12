from django.db import models

from texter.models import PhoneNumberField, AbstractBackend, Backend


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
                delegate_classname=self.qualified_classname,
                delegate_pk=self.pk,
                name=self._name)
        else:
            b = Backend.objects.get(
                delegate_classname=self.qualified_classname,
                delegate_pk=self.pk)
            b.name = self._name
            b.save()
