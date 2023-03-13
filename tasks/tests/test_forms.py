import datetime
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..forms import TaskForm
from ..models import Task,Stage,Priority


User = get_user_model()


class TaskCreateAndEditFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.stage = Stage.objects.create(name="Stage 1")
        cls.priority = Priority.objects.create(name="Priority 1")
        cls.form = TaskForm()

    def setUp(self):
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создаст запись в таблице Tasks."""
        count_tasks = Task.objects.count()
        form_data = {
            'title': 'title',
            'description': 'description',
            'start_task': datetime.datetime.now(),
            'complate_task': datetime.datetime.now(),
            'stage': self.stage.pk,
            'priority': self.priority.pk,
            'worker': self.user
        }
        response = self.authorized_client_author.post(
            reverse('tasks:task_create'),
            data=form_data,
            follow=True,
        )
        task = Task.objects.first()
        self.assertRedirects(response, reverse(
            'tasks:tasks', kwargs={'username': self.user.username}
            )
        )
        self.assertEqual(Task.objects.count(), count_tasks + 1)
        self.assertEqual(task.title, form_data['title'])
        self.assertEqual(task.description, form_data['description'])
        self.assertEqual(task.stage.pk, form_data['stage'])
        self.assertEqual(task.priority.pk, form_data['priority'])
        self.assertEqual(task.worker, form_data['worker'])
