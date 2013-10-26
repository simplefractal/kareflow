# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.query import QuerySet
from django.db.models import Manager


class TaskQuerySet(QuerySet):

    def open(self):
        return self.filter(status=1)

    def completed(self):
        return self.filter(status=10)


class TaskManager(Manager):

    def get_query_set(self):
        return TaskQuerySet(self.model)
