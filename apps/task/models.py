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

    @property
    def is_call(self):
        return self.action == 1

    @property
    def is_schedule(self):
        return self.action == 2

    @property
    def is_visit(self):
        return self.action == 3

    @property
    def display_text(self):
        if self.is_call:
            return "Call {} by {}".format(self.patient.name, self.deadline)
        else:
            return "Schedule visit for {} by {}".format(
                self.patient.name, self.deadline)

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
