# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib.humanize.templatetags.humanize import naturaltime

from django.db import models
from util.randz import make_8_key

from .managers import TaskManager


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

    objects = TaskManager()

    def __unicode__(self):
        return "{}: {}".format(self.patient.name, self.action)

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
            return "Call {} at {}".format(
                self.patient.name,
                self.patient.phone_cell)
        else:
            return "Schedule {} a visit before {}".format(
                self.patient.name,
                self.deadline.strftime("%m/%d"))

    @property
    def action_deadline(self):
        """
        This is the deadline for the staff member to complete the task.
        For scheduling a visit, the deadline is 2 days after the task was added,
        even though the visit must take place within 7 or 14 days. The 7 or 14 day
        endpoint is the deadline, while 2 days is the action_deadline.
        """
        if self.is_schedule:
            return datetime.datetime(
                self.date_added.year,
                self.date_added.month,
                self.date_added.day,
                self.date_added.hour,
                self.date_added.minute) + datetime.timedelta(days=2)
        else:
            return self.deadline

    @property
    def action_deadline_text(self):
        text = naturaltime(self.action_deadline)
        text = text.replace("ago", "late")
        text = text.replace("from now", "left")
        return text

    @property
    def is_urgent(self):
        """
        Less than a day to complete.
        """
        # TODO fix hack to avoid tz awareness
        action_deadline = datetime.datetime(
            self.action_deadline.year,
            self.action_deadline.month,
            self.action_deadline.day,
            self.action_deadline.hour,
            self.action_deadline.minute)
        return ((action_deadline - datetime.datetime.now())
                .total_seconds() < 60 * 60 * 24)

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
