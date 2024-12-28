import django_filters
from django import forms
from django.contrib.auth import get_user_model

from task_manager.label.models import Label
from task_manager.status.models import Status

from .models import Task

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'author']

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label_suffix='',
        label='Статус'
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label_suffix='',
        label='Исполнитель',
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label_suffix='',
        label='Метка',
    )
    author = django_filters.BooleanFilter(
        method='author_filter',
        widget=forms.CheckboxInput(),
        label_suffix='',
        label='Только свои задачи',
    )

    def author_filter(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
