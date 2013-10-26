# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models

from util.randz import make_8_key
from util.stringz import format_phone


class Address(models.Model):
    street_1 = models.CharField(max_length=100)
    street_2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default="United States")

    def __unicode__(self):
        return "{}, {}, {} {}, {}".format(
            self.street_1, self.city, self.state, self.zip_code, self.country)

    def to_json(self):
        return {
            'street1': self.street_1,
            'street2': self.street_2,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
        }


class Patient(models.Model):
    uuid = models.CharField(blank=True, unique=True, max_length=50)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    # Demographics
    ssn = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)

    # Contact info
    phone_home = models.CharField(max_length=15, null=True, blank=True)
    phone_work = models.CharField(max_length=15, null=True, blank=True)
    phone_cell = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    address = models.ForeignKey('patient.Address', null=True, blank=True)

    insurance = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return "{}, {}".format(self.last_name, self.first_name)

    @property
    def name(self):
        return u"{} {}".format(self.first_name, self.last_name)

    @property
    def age(self):
        if not self.dob:
            return
        now = datetime.datetime.now()
        dob = datetime.datetime(self.dob.year, self.dob.month, self.dob.day)
        total_seconds = (now - dob).total_seconds()
        # return the integer number of years since DOB to now
        return int(total_seconds / (60 * 60 * 24 * 365))

    @property
    def phone(self):
        if self.phone_cell:
            return self.phone_cell
        elif self.phone_home:
            return self.phone_work
        else:
            return self.phone_home

    @property
    def status(self):
        """
        Smart property displaying the current
        status of the patient based on recent
        events
        """
        # TODO: implement
        return "in Jupiter ER"

    def to_json(self):
        return {
            "name": self.name,
            "age": self.age,
            "status": self.status,
            "uuid": self.uuid,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "name": self.name,
            "ssn": self.ssn,
            "dob": self.dob and self.dob.strftime('%m/%d/%Y'),
            "sex": self.sex,
            "maritalStatus": self.marital_status,
            "phoneHome": format_phone(self.phone_home),
            "phoneWork": format_phone(self.phone_work),
            "phoneCell": format_phone(self.phone_cell),
            "email": self.email,
            "address": self.address and self.address.to_json(),
            "insurance": self.insurance,
        }

    def save(self, *args, **kwargs):
        """
        Ensure unique uuid
        """
        if not self.uuid:
            uuid = make_8_key()
            while Patient.objects.filter(uuid=uuid).exists():
                uuid = make_8_key()
            self.uuid = uuid
        super(Patient, self).save(*args, **kwargs)
