from django.views.generic import TemplateView

from .models import Task


class TaskList(TemplateView):
    template_name = "task_list.html"

    def get_context_data(self, *args, **kwargs):
        return {
            "tasks": Task.objects.all().order_by("deadline")
        }

task_list = TaskList.as_view()
