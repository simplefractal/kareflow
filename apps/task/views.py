from django.views.generic import TemplateView

from .models import Task


class TaskList(TemplateView):
    template_name = "task_list.html"

    def get_context_data(self, *args, **kwargs):
        return {
            "tasks": sorted(
                list(
                    Task.objects.all()),
                key=lambda task: task.action_deadline)
        }

task_list = TaskList.as_view()
