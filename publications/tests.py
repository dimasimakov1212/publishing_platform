from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from publications.models import Publication
from users.models import User


class PublicationTestCase(TestCase):

    def setUp(self) -> None:

        # создаем тестового пользователя
        self.user = User.objects.create(user_email='admin@dima.pro')
        self.user.set_password('dima123')
        self.user.save()

        self.client = Client()

        # создаем тестовую публикацию
        self.publication = Publication.objects.create(
            publication_title='Test',
            publication_text='Test',
            publication_price='10',
            publication_owner=self.user
        )

        self.publication = Publication.objects.create(
            publication_title='Test_1',
            publication_text='Test_1',
            publication_price='20',
            publication_owner=self.user
        )

        # аутентификацируем пользователя
        # login = self.client.login(user_email='admin@dima.pro', password='dima123')

    def test_create_publication(self):
        """ Тестирование создания публикации """

        publication = Publication.objects.create(
            publication_title='Test',
            publication_text='Test',
            publication_price=10,
            publication_owner=self.user
        )

        publication_title = publication.publication_title
        publication_text = publication.publication_text
        publication_price = publication.publication_price
        publication_owner = publication.publication_owner

        self.assertEquals(publication_title, 'Test')
        self.assertEquals(publication_text, 'Test')
        self.assertEquals(publication_price, 10.00)
        self.assertEquals(publication_owner, self.user)

        # проверяем на существование объектов публикаций
        self.assertTrue(
            Publication.objects.all().exists()
        )

    # def test_list_publication(self):
    #     """ Тестирование списка публикаций """
    #
    #     self.user = User.objects.create(user_email='dima@dima.pro')
    #     self.user.set_password('dima123')
    #     self.user.save()
    #
    #     user = authenticate(user_email='dima@dima.pro', password='dima123')
    #     login(self, user)
    #
    #     Publication.objects.create(
    #         publication_title='Test_1',
    #         publication_text='Test_1',
    #         publication_price='20',
    #         publication_owner=self.user
    #     )
    #
    #     # аутентифицируем пользователя
    #     # login = self.client.login(user_email='admin@dima.pro', password='dima123')
    #
    #     response = self.client.get('/homepage/')
    #     self.assertEqual(response.status_code, 200)

    def test_detail_publication(self):
        """ Тестирование деталей публикации """

        publication = Publication.objects.create(
            publication_title='Test',
            publication_text='Test',
            publication_price='10',
            publication_owner=self.user
        )

        response = self.client.get(
            reverse('publications:publication_detail', kwargs={'pk': publication.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_change_publication(self):
        """ Тестирование изменения публикации """

        publication = Publication.objects.create(
            publication_title='Test',
            publication_text='Test',
            publication_price='10',
            publication_owner=self.user
        )

        response = self.client.post(
            reverse('publications:publication_edit',
                    kwargs={'pk': publication.pk}), {'publication_title': 'Test_1'})

        self.assertEqual(response.status_code, 200)

    def test_delete_publication(self):
        """ Тестирование удаления публикации """

        publication = Publication.objects.create(
            publication_title='Test',
            publication_text='Test',
            publication_price='10',
            publication_owner=self.user
        )

        response = self.client.get(
            reverse('publications:publication_delete',
                    kwargs={'pk': publication.pk}))

        self.assertEqual(response.status_code, 200)

    def test_main_page_publication(self):
        """ Тестирование главной страницы """

        response = self.client.get('')
        self.assertTemplateUsed(response, 'publications/homepage.html')

    def test_user_publication(self):
        """ Тестирование страницы списка публикаций пользователя """

        response = self.client.get('/finish_subscription/')
        self.assertTemplateUsed(response, 'publications/finish_subscription.html')

    def test_other_users_page_publication(self):
        """ Тестирование страницы списка публикаций других пользователей """

        self.user = User.objects.create(user_email='admin_2@dima.pro')
        self.user.set_password('dima123')
        self.user.save()

        response = self.client.get(
            reverse('publications:other_user_publications',
                    kwargs={'pk': self.user.pk}))

        self.assertTemplateUsed(response, 'publications/publications_list.html')
        self.assertEqual(response.status_code, 200)
