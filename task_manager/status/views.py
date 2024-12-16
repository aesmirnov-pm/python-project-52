from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import DeleteErrorMixin
from .forms import StatusForm
from .models import Status


# ALL STATUSES page
class StatusView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    ordering = ['id']


# CREATE STATUS page
class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/new_status.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Статус создан'


# UPDATE STATUS page
class StatusUpdateFormView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Статус обновлен'


# DELETE STATUS page
class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteErrorMixin,
                       DeleteView):
    model = Status
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Статус удален'
    reject_message = 'You cannot delete the status that is used in a task'
