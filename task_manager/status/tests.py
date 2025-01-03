from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Status

User = get_user_model()


class StatusTest(TestCase):

    def setUp(self):
        self.statuses = Status.objects.all()
        self.username = 'testuser'
        self.password = '12345'
        self.status = 'test_status'
        self.status_upd = 'test_status_upd'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_create_status_db(self):
        Status.objects.create(name=self.status)
        self.assertEqual(self.statuses.count(), 1)
        self.assertEqual(self.statuses.first().name, self.status)

    def test_create_status_form(self):
        response_create_status = self.client.post('/statuses/create/',
                                                  follow=True,
                                                  data={'name': self.status})
        self.assertContains(response_create_status,
                            'Статус успешно создан',
                            status_code=200)
        self.assertEqual(self.statuses.count(), 1)
        self.assertEqual(self.statuses.first().name, self.status)

    def test_update_status_form(self):
        Status.objects.create(name=self.status)
        response_update_status = (
            self.client.post('/statuses/1/update/',
                             follow=True,
                             data={'name': self.status_upd}))
        self.assertContains(response_update_status,
                            'Статус успешно изменен',
                            status_code=200)
        self.assertEqual(self.statuses.first().name, self.status_upd)

    def test_status_delete_form(self):
        Status.objects.create(name=self.status)
        response_delete_status = self.client.post('/statuses/1/delete/',
                                                  follow=True)
        self.assertContains(response_delete_status,
                            'Статус успешно удален',
                            status_code=200)
        self.assertEqual(self.statuses.count(), 0)
