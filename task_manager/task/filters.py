import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.label.models import Label
from task_manager.status.models import Status
from task_manager.user.models import User
from .models import Task


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'author']

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label_suffix='',
        label=_('Статус')
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label_suffix='',
        label=_('Исполняющий'),
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label_suffix='',
        label=_('Метки'),
    )
    author = django_filters.BooleanFilter(
        method='author_filter',
        widget=forms.CheckboxInput(),
        label_suffix='',
        label=_('Только мои задачи'),
    )

    def author_filter(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
