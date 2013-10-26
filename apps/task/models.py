# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from util.randz import make_8_key


ACTION_CHOICES = (
    (1, "Call patient"),
    (2, "Schedule visit for patient"),
    (3, "See patient in office"),
)


TASK_STATUSES = (
    (1, "Incomplete"),
    (10, "Complete"),
)


class Task(models.Model):
    uuid = models.CharField(blank=True, unique=True, max_length=50)
    patient = models.ForeignKey("patient.Patient")
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES, default=1)
    deadline = models.DateTimeField()
    date_completed = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    providers = models.ManyToManyField("provider.Provider")
    status = models.PositiveSmallIntegerField(choices=TASK_STATUSES, default=1)
    marked_complete_by = models.ForeignKey("account.Account", blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Ensure unique uuid
        """
        if not self.uuid:
            uuid = make_8_key()
            while Task.objects.filter(uuid=uuid).exists():
                uuid = make_8_key()
            self.uuid = uuid
        super(Task, self).save(*args, **kwargs)
