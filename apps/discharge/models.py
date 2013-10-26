# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json_field import JSONField

from django.db import models
from util.randz import make_8_key


class Discharge(models.Model):
    uuid = models.CharField(blank=True, unique=True, max_length=50)

    # Message
    date = models.DateTimeField(null=True, blank=True)
    facility = models.CharField(max_length=100, null=True, blank=True)
    diagnosis = models.CharField(max_length=50, null=True, blank=True)

    # Patient
    patient = models.ForeignKey('patient.Patient')
    metadata = JSONField(null=True, blank=True)

    # Doctors
    attending = models.ForeignKey('provider.Provider', related_name="attending", null=True, blank=True)
    referring = models.ForeignKey('provider.Provider', related_name="referring", null=True, blank=True)

    def __unicode__(self):
        return u"{} ({})".format(
            self.patient,
            self.date.strftime("%m/%d/%y"))

    def save(self, *args, **kwargs):
        """
        Ensure unique uuid
        """
        if not self.uuid:
            uuid = make_8_key()
            while Discharge.objects.filter(uuid=uuid).exists():
                uuid = make_8_key()
            self.uuid = uuid
        super(Discharge, self).save(*args, **kwargs)
