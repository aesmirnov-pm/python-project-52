from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.label.models import Label
from task_manager.status.models import Status
from .models import Task

User = get_user_model()


class TaskTest(TestCase):

    def setUp(self):
        self.tasks = Task.objects.all()
        self.username = 'testuser'
        self.password = '12345'
        self.task_name = 'test_task'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.status = Status.objects.create(name='test_status')
        self.label = Label.objects.create(name='test_label')

    def test_create_task_db(self):
        task = Task.objects.create(name=self.task_name, status=self.status,
                                   author=self.user, executor=self.user)
        task.labels.add(self.label)
        self.assertTrue(Task.objects.filter(
            name=self.task_name,
            status=self.status,
            executor=self.user,
            author=self.user).exists())
        self.assertTrue(all((
            self.tasks.first().name == self.task_name,
            self.tasks.first().status == self.status,
            self.tasks.first().executor == self.user,
            self.tasks.first().author == self.user,
        )))

    def test_create_task_form(self):
        response_create_task = (
            self.client.post('/tasks/create/',
                             follow=True,
                             data={
                                 'name': self.task_name,
                                 'description': self.task_name,
                                 'status': self.status.id,
                                 'author': self.user.id,
                                 'executor': self.user.id,
                             }))
        self.assertContains(response_create_task,
                            'Задача успешно создана',
                            status_code=200)
        self.assertEqual(self.tasks.count(), 1)
        self.assertTrue(all((
            self.tasks.first().name == self.task_name,
            self.tasks.first().status == self.status,
            self.tasks.first().executor == self.user,
            self.tasks.first().author == self.user,
        )))

    def test_update_task_form(self):
        Task.objects.create(name=self.task_name, status=self.status,
                            author=self.user, executor=self.user)
        response_update_task = (
            self.client.post('/tasks/1/update/',
                             follow=True,
                             data={
                                 'name': self.task_name,
                                 'description': self.task_name,
                                 'status': self.status.id,
                                 'author': self.user.id,
                                 'executor': self.user.id,
                             }))
        self.assertContains(response_update_task,
                            'Задача успешно изменена',
                            status_code=200)
        self.assertTrue(self.tasks.first().description == self.task_name)

    def test_task_delete_form(self):
        Task.objects.create(name=self.task_name, status=self.status,
                            author=self.user, executor=self.user)
        response_delete_task = self.client.post('/tasks/1/delete/',
                                                follow=True)
        self.assertContains(response_delete_task,
                            'Задача успешно удалена',
                            status_code=200)
        self.assertEqual(self.tasks.count(), 0)
