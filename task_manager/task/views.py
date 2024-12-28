from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import HandleNoPermissionMixin
from task_manager.task.mixins import TaskDeletionPermitMixin

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


# ALL TASKS page
class TaskView(LoginRequiredMixin, FilterView):
    filterset_class = TaskFilter
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'


# CREATE TASK page
class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/new_task.html'
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)


# UPDATE TASK page
class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно изменена'


# DELETE TASK page
class TaskDeleteView(SuccessMessageMixin, HandleNoPermissionMixin, TaskDeletionPermitMixin,
                     DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно удалена'


# TASK DETAILS page
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/view_task.html'
    context_object_name = 'task'
