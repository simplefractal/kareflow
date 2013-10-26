from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Task


class TaskList(TemplateView):
    template_name = "task_list.html"

    def get_context_data(self, *args, **kwargs):
        tasks = Task.objects.all()
        if self.request.GET.get("completed"):
            active_filter = "completed"
            tasks = tasks.completed()
        else:
            tasks = tasks.open()
            active_filter = "open"
        return {
            "active_filter": active_filter,
            "tasks": sorted(
                list(tasks),
                key=lambda task: task.action_deadline)
        }


class MarkComplete(View):
    def get(self, request, task_uuid):
        task = get_object_or_404(Task, uuid=task_uuid)
        task.mark_complete()
        return HttpResponseRedirect(reverse('task_list'))


class MarkOpen(View):
    def get(self, request, task_uuid):
        task = get_object_or_404(Task, uuid=task_uuid)
        task.mark_open()
        return HttpResponseRedirect(reverse('task_list'))


task_list = TaskList.as_view()
mark_complete = MarkComplete.as_view()
mark_open = MarkOpen.as_view()
