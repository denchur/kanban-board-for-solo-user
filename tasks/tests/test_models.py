from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Priority, Stage, Task

User = get_user_model()


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username = 'testuser',
        )
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
            worker = cls.user,
        )

    def test_task_str(self):
        """Проверка метода __str__ у класса Task"""
        self.assertEqual(str(self.task), self.task.title)
        
    def test_priority_str(self):
        """Проверка метода __str__ у класса Priority"""
        self.assertEqual(str(self.priority), self.priority.name)

    def test_stage_str(self):
        """Проверка метода __str__ у класса Stage"""
        self.assertEqual(str(self.stage), self.stage.name)
