# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from util.randz import make_8_key


class Account(models.Model):
    user = models.OneToOneField("auth.user", null=True)
    uuid = models.CharField(blank=True, unique=True, max_length=50)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    providers = models.ManyToManyField("provider.Provider")

    def save(self, *args, **kwargs):
        """
        Ensure unique uuid
        """
        if not self.uuid:
            uuid = make_8_key()
            while Account.objects.filter(uuid=uuid).exists():
                uuid = make_8_key()
            self.uuid = uuid
        super(Account, self).save(*args, **kwargs)
