from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self, **kwargs):
        self.users = User.objects.all()
        self.username, self.first_name, self.last_name = 'testuser', 'tester', 'testoff'
        self.password = 'qwe123qwe1'
        self.form_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
        }
        self.form_data_1 = {
            'id': self.users[0].id,
            'first_name': self.users[0].first_name,
            'last_name': self.users[0].last_name,
            'username': self.users[0].username,
            'password1': self.password,
            'password2': self.password,
        }
        self.form_data_2 = {
            'id': self.users[1].id,
            'first_name': self.users[1].first_name,
            'last_name': self.users[1].last_name,
            'username': self.users[1].username,
            'password1': self.password,
            'password2': self.password,
        }

    def test_create_user_form(self):
        response_register_user = self.client.post('/users/create/',
                                                  follow=True,
                                                  data=self.form_data)
        self.assertContains(response_register_user,
                            'Пользователь успешно зарегистрирован',
                            status_code=200)

        self.assertIsNotNone(User.objects.filter(
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
        ))

    def test_create_unique_user_form(self):
        User.objects.create_user(first_name=self.first_name,
                                 last_name=self.last_name,
                                 username=self.username,
                                 password=self.password)

        response_register_user = self.client.post('/users/create/',
                                                  follow=True,
                                                  data=self.form_data)
        self.assertEqual(response_register_user.status_code, 200)
        self.assertIsNotNone(User.objects.filter(username=self.username))

    def test_user_update_form(self):
        self.client.login(username=self.form_data_1['username'],
                          password=self.form_data_1['password1'])
        response_update_user = self.client.post('/users/{}/update/'.format(self.form_data_1['id']),
                                                follow=True,
                                                data=self.form_data)
        self.assertContains(response_update_user, 'Пользователь успешно изменен', status_code=200)

        self.assertEqual(User.objects.get(
            id=self.form_data_1['id']).username, self.username)

    def test_user_delete_form(self):
        self.client.login(username=self.form_data_1['username'],
                          password=self.form_data_1['password1'])
        response_delete_user = self.client.post('/users/{}/delete/'.format(self.users[0].id),
                                                follow=True)
        self.assertContains(response_delete_user, 'Пользователь успешно удален', status_code=200)
        self.assertEqual(User.objects.filter(
            username=self.form_data_1['username']).exists(), False)

    def test_login_right_form(self):
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        response_login_user = self.client.post('/login/',
                                               follow=True,
                                               data={
                                                   'username': self.username,
                                                   'password': self.password,
                                               })
        self.assertContains(
            response_login_user,
            'Вы залогинены',
            status_code=200,
        )
        self.assertTrue(self.user.is_authenticated)

    def test_login_unexistent_user_form(self):
        response_login_user = self.client.post('/login/',
                                               data={
                                                   'username': self.username,
                                                   'password': self.password
                                               })
        self.assertContains(
            response_login_user,
            'Введите корректное имя пользователя и парооль.',
            status_code=200
        )

    def test_user_unauthorized(self):
        self.client.login(username=self.form_data_1['username'],
                          password=self.form_data_1['password1'])
        response_delete_user = self.client.post('/users/{}/delete/'.format(self.users[1].id),
                                                follow=True)
        self.assertContains(response_delete_user,
                            'У вас нет прав для изменения другого пользователя.',
                            status_code=200)

        response_update_user = self.client.post('/users/{}/update/'.format(self.users[1].id),
                                                follow=True,
                                                data=self.form_data_2)
        self.assertContains(response_update_user,
                            'У вас нет прав для изменения другого пользователя.',
                            status_code=200)
