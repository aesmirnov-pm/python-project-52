from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import DeleteErrorMixin
from .forms import LabelForm
from .models import Label


# ALL LABELS page
class LabelView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    ordering = ['id']


# CREATE LABEL page
class LabelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/new_label.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно создана'


# UPDATE LABEL page
class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно изменена'


# DELETE STATUS page
class LabelDeleteView(SuccessMessageMixin,
                      LoginRequiredMixin,
                      DeleteErrorMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно удалена'
    reject_message = 'Невозможно удалить метку'
