from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from payments.models import Product, Payment
from publications.models import Publication
from users.models import User


class PaymentTestCase(TestCase):

    def setUp(self) -> None:

        # создаем тестового пользователя
        self.user = User.objects.create(user_email='admin@dima.pro')
        self.user.set_password('dima123')
        self.user.save()

        self.client = Client()

    def test_create_product(self):
        """ Тестирование создания продукта """

        product = Product.objects.create(
            product_name='Test',
            product_price=200,
        )
        product.save()

        publication = Publication.objects.create(
            publication_title='Test',
            publication_text='Test',
            publication_price=10,
            publication_owner=self.user
        )
        publication.save()

        payment = Payment.objects.create(
            payment_user=self.user,
            payment_publication=publication,
            payment_product=product
        )
        payment.save()

        product_name = product.product_name
        product_price = product.product_price

        payment_user = payment.payment_user
        payment_publication = payment.payment_publication
        payment_product = payment.payment_product

        self.assertEquals(product_name, 'Test')
        self.assertEquals(product_price, 200)
        self.assertEquals(payment_user, self.user)
        self.assertEquals(payment_publication, publication)
        self.assertEquals(payment_product, product)

    def test_success_page(self):
        """ Тестирование страницы успешной оплаты """

        response = self.client.get('/payments/success/')
        self.assertTemplateUsed(response, 'payments/success.html')

    def test_cancel_page(self):
        """ Тестирование страницы ошибки оплаты """

        response = self.client.get('/payments/cancel/')
        self.assertTemplateUsed(response, 'payments/cancel.html')

    def test_landing_page(self):
        """ Тестирование страницы перенаправления на stripe """

        product = Product.objects.create(
            product_name='Test',
            product_price=200,
        )
        product.save()

        response = self.client.get(
            reverse('payments:landing',
                    kwargs={'pk': product.pk}))
        self.assertTemplateUsed(response, 'payments/landing.html')
        self.assertTrue(response.status_code == 200)
