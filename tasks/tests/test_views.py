import datetime
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms

from ..models import Task,Priority,Stage

User = get_user_model()

class TestTaskTemplate(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='testuser')
        cls.stage = Stage.objects.create(name="Stage 1")
        cls.priority = Priority.objects.create(name="Priority 1")
        cls.task = Task.objects.create(
            title = 'title',
            description = 'description',
            start_task = datetime.datetime.now(),
            stage  = cls.stage,
            priority = cls.priority,
            worker = cls.user
        )
    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(self.user)
    
    def TestViewsUseNecessaryTemplates(self):
        templates_pages_names = {
            reverse('tasks:home_page'):'tasks/index.html',
            reverse('tasks:tasks', kwargs = {'username': self.auth_client}):'tasks/tasks.html',
            reverse('tasks:task_detail', kwargs = {'task_id': self.task.pk}):'tasks/task_detail.html',
            reverse('tasks:task_create'):'tasks/task_create.html',
            reverse('tasks:task_edit', kwargs={'task_id': self.task.pk}):'tasks/task_create.html',
            reverse('tasks:update_stage', kwargs={'task_id': self.task.pk}):'tasks/task_create.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.auth_client.get(reverse_name)
                self.assertTemplateUsed(response, template)