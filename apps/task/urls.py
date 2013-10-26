# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'task.views.task_list', name='task_list'),
    url(r'^complete/(?P<task_uuid>\w+)/$', 'task.views.mark_complete', name='mark_complete'),
    url(r'^open/(?P<task_uuid>\w+)/$', 'task.views.mark_open', name='mark_open'),
)
