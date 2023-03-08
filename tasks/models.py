from django.db import models
from django.contrib.auth import get_user_model

import datetime

User = get_user_model()


class Priority(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Stage(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(
        max_length= 100,
        verbose_name= "Название задчи"
        )
    description = models.TextField(
        verbose_name= "Описание задчи"
        )
    start_task = models.DateTimeField(
        auto_now_add= False,
        default= datetime.datetime.now(),
        verbose_name= 'Дата создания задчи',
    )
    complate_task = models.DateTimeField(
        auto_now_add= False,
        null=True,
        blank=True,
        verbose_name= 'Дата завершения задчи',
    )
    stage = models.ForeignKey(
        Stage,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks',
        verbose_name="Стадия выполнения задачи",
        default= 1,
        )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Приоритет задачи",
        default=1,
        )
    worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Владелец задачи"
    )
    class Meta:
        ordering = ['-priority']


    def __str__(self):
        return self.title
          

