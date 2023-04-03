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
        auto_now_add= True,
        verbose_name= 'Дата создания задчи',
    )
    dedline_task = models.DateTimeField(
        auto_now_add= False,
        null=True,
        blank=True,
        verbose_name= 'Дата планируемого дедлайна',
    )
    complate_task = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name = 'Дата завершения задачи',
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


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    creted = models.DateField(auto_now_add=True)

