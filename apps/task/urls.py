# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'task.views.task_list', name='task_list'),
)
