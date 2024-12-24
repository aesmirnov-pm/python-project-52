from django.contrib.auth import get_user_model
from django.db import models

from task_manager.label.models import Label
from task_manager.status.models import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        verbose_name='name',
        max_length=150,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='status_tasks',
        verbose_name='Status',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author_tasks',
        verbose_name='Author',
    )
    executor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='executor_tasks',
        verbose_name='Executor',
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        through='Labeled',
        verbose_name='Labels',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Labeled(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
