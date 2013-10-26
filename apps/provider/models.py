# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from util.randz import make_8_key


ROLE_CHOICES = (
    (1, "Other"),
    (2, "Nurse"),
    (3, "PCP"),
    (4, "Specialist"),
)


class Provider(models.Model):
    user = models.OneToOneField("auth.user", null=True)
    uuid = models.CharField(blank=True, unique=True, max_length=50)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)

    def __unicode__(self):
        return "Dr. {}, {}".format(self.last_name, self.first_name)

    @property
    def name(self):
        return u"{} {}".format(self.first_name, self.last_name)

    def to_json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": dict(ROLE_CHOICES).get(self.role),
        }

    def save(self, *args, **kwargs):
        """
        Ensure unique uuid
        """
        if not self.uuid:
            uuid = make_8_key()
            while Provider.objects.filter(uuid=uuid).exists():
                uuid = make_8_key()
            self.uuid = uuid
        super(Provider, self).save(*args, **kwargs)
