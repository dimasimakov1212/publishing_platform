from django.test import TestCase
from django.test.client import Client

from django.core.management import call_command

from users.models import User
from users.services import code_generator


class UserTestCase(TestCase):

    def setUp(self) -> None:

        # создаем тестового пользователя
        self.user = User.objects.create(user_email='admin@dima.pro', user_phone='+70000000000')
        self.user.set_password('dima123')
        self.user.save()

        self.client = Client()

        # аутентификацируем пользователя
        # login = self.client.login(user_email='admin@dima.pro', password='dima123')

    def test_create_user(self):
        """ Тестирование создания пользователя """

        user_email = self.user.user_email
        user_phone = self.user.user_phone
        is_active = self.user.is_active

        self.assertEquals(user_email, 'admin@dima.pro')
        self.assertEquals(user_phone, '+70000000000')
        self.assertEquals(is_active, False)

        # проверяем на существование объектов публикаций
        self.assertTrue(
            User.objects.all().exists()
        )

    # def test_detail_user(self):
    #     """ Тестирование деталей пользователя """
    #
    #     self.user = User.objects.create(user_email='admin_1@dima.pro', user_phone='+70000000000')
    #     self.user.set_password('dima123')
    #     # self.user.authenticate(user_email='admin_1@dima.pro', password='dima123')
    #     login(self, self.user)
    #
    #     response = self.client.get(
    #         reverse('users:profile', kwargs={'pk': self.user.pk})
    #     )
    #
    #     self.assertEqual(response.status_code, 200)

    def test_user_confirmed(self):
        """ Тестирование страницы подтверждения регистрации пользователя """

        response = self.client.get('/users/user_confirmed/')
        self.assertTemplateUsed(response, 'users/user_confirmed.html')

    def test_code_generator(self):
        """ Тестирование генератора кода """

        code_1 = code_generator()

        self.assertEquals(len(code_1), 4)


class CommandsTestCase(TestCase):

    def test_mycommand(self):
        """ Тестирование создания суперпользователя """

        args = []
        opts = {}
        call_command('create_super_user', *args, **opts)
