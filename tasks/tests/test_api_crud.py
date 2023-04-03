import datetime
from http import HTTPStatus
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
        cls.task = Task.objects.create(
            title = 'Test Task',
            description = 'Test description',
            stage = cls.stage,
            priority = cls.priority,
            worker = cls.user,
        )
        cls.form = TaskForm()

    def setUp(self):
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user)
        self.no_auth_client = Client()

    def test_auth_user_create__post(self):
        """Авторизированный пользователь может создать запись в таблице Tasks."""
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
        self.assertEqual(response.status_code, HTTPStatus.OK)
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

    def test_no_auth_user_create__post(self):
        """Неавторизованный пользователь не может создать запись в таблице Tasks."""
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
        response = self.no_auth_client.post(
            reverse('tasks:task_create'),
            data=form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'
            )+'?next=/create/'
        )
        self.assertEqual(Task.objects.count(), count_tasks)
    
    def test_auth_user_author_delete_task(self):
        '''Авторизированный пользователь может удалить запись из таблицы Tasks'''
        count_tasks = Task.objects.count()
        response = self.authorized_client_author.post(
            reverse('tasks:delete_task', kwargs = {'task_id':self.task.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.count(), count_tasks-1)
        self.assertRedirects(response, reverse('tasks:tasks', kwargs = {'username':self.user}))
    
    def test_no_auth_user_author_delete_task(self):
        '''Неавторизованный пользователь не может удалить запись из таблицы Tasks'''
        count_tasks = Task.objects.count()
        response = self.no_auth_client.post(
            reverse('tasks:delete_task', kwargs = {'task_id':self.task.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.count(), count_tasks)
        self.assertRedirects(response, reverse('users:login'
            )+'?next=/task/1/delete/'
        )
    
    def test_correct_context(self):
        respone =  self.authorized_client_author.get(reverse('tasks:tasks', kwargs = {'username':self.user}))
        task = respone.context['task_stage_one'][0]
        self.assertEqual(task.title, self.task.title)
        self.assertEqual(task.description, self.task.description)
        self.assertEqual(task.stage, self.task.stage)
        self.assertEqual(task.priority, self.task.priority)


