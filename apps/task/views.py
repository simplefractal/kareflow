from django.views.generic import TemplateView

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

task_list = TaskList.as_view()
