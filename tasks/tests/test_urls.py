from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Priority, Stage, Task

User = get_user_model()


class TaskUrlsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.noauthor = User.objects.create_user(username='auth')
        cls.priority = Priority.objects.create(
            name='test priority',
        )
        cls.stage = Stage.objects.create(
            name = 'test stage',
        )
        cls.task =  Task.objects.create(
            title = 'test task',
            description = 'test description',
            start_task = '2020-01-01',
            complate_task = '2020-01-02',
            stage = cls.stage,
            priority = cls.priority,
            worker = cls.author,
        )
    
    def setUp(self):
        self.guest_client = Client()
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.author)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.noauthor)
    
    def test_urls_no_auth(self):
        """Провеерка доступа к страницам проекта
            для неаторизированного пользователя."""
        respone_urls_code = {
            reverse('tasks:home_page'):HTTPStatus.FOUND,
            reverse('tasks:tasks', kwargs = {'username': self.authorized_client_author}):HTTPStatus.FOUND,
            reverse('tasks:task_detail', kwargs = {'task_id': self.task.pk}):HTTPStatus.FOUND,
            reverse('tasks:task_create'):HTTPStatus.FOUND,
            reverse('tasks:task_edit', kwargs={'task_id': self.task.pk}):HTTPStatus.FOUND,
            reverse('tasks:update_stage', kwargs={'task_id': self.task.pk}):HTTPStatus.FOUND,
            reverse('tasks:delete_task', kwargs={'task_id': self.task.pk}):HTTPStatus.FOUND,
        }
        for url, code in respone_urls_code.items():
            with self.subTest(url=url):
                status_code = self.guest_client.get(url).status_code
                self.assertEqual(status_code, code)
    
    def test_urls_auth_no_author(self):
        """Провеерка доступа к страницам проекта
            для авторизированного пользователя 
            не являющегося автором тестируемых задач."""
        respone_urls_code = {
            reverse('tasks:home_page'):HTTPStatus.FOUND,
            reverse('tasks:tasks', kwargs = {'username': self.authorized_client_author}):HTTPStatus.NOT_FOUND,
            reverse('tasks:task_detail', kwargs = {'task_id': self.task.pk}):HTTPStatus.FOUND,
            reverse('tasks:task_create'):HTTPStatus.OK,
            reverse('tasks:task_edit', kwargs={'task_id': self.task.pk}):HTTPStatus.FOUND,
            reverse('tasks:update_stage', kwargs={'task_id': self.task.pk}):HTTPStatus.FOUND,
            reverse('tasks:delete_task', kwargs={'task_id': self.task.pk}):HTTPStatus.FOUND,
        }
        for url, code in respone_urls_code.items():
            with self.subTest(url=url):
                status_code = self.authorized_client.get(url).status_code
                self.assertEqual(status_code, code)
    
    def test_urls_auth_author(self):
        """Провеерка доступа к страницам проекта
            для авторизированного пользователя 
            являющегося автором тестируемых задач."""
        respone_urls_code = {
            reverse('tasks:home_page'):HTTPStatus.FOUND,
            reverse('tasks:tasks', kwargs = {'username': self.authorized_client_author}):HTTPStatus.NOT_FOUND,
            reverse('tasks:task_detail', kwargs = {'task_id': self.task.pk}):HTTPStatus.OK,
            reverse('tasks:task_create'):HTTPStatus.OK,
            reverse('tasks:task_edit', kwargs={'task_id': self.task.pk}):HTTPStatus.OK,
            reverse('tasks:update_stage', kwargs={'task_id': self.task.pk}):HTTPStatus.OK,
            reverse('tasks:delete_task', kwargs={'task_id': self.task.pk}):HTTPStatus.FOUND,
        }
        for url, code in respone_urls_code.items():
            with self.subTest(url=url):
                status_code = self.authorized_client_author.get(url).status_code
                self.assertEqual(status_code, code)
    
    

        
        

