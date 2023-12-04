from django.conf import settings
from django.db import models

from publications.models import Publication


class Product(models.Model):
    """ Модель продукта для оплаты """

    product_name = models.CharField(max_length=100, verbose_name='продукт')
    product_price = models.IntegerField(default=0, verbose_name='цена')  # cents

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'продукт'  # Настройка для наименования одного объекта
        verbose_name_plural = 'продукты'  # Настройка для наименования набора объектов
        ordering = ('id',)  # сортировка


class Payment(models.Model):
    """ Модель платежа """

    payment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='плательщик')
    payment_publication = models.ForeignKey(Publication, on_delete=models.CASCADE, verbose_name='публикация',
                                            blank=True, null=True)
    payment_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт оплаты',
                                        blank=True, null=True)

    def __str__(self):
        return self.payment_product

    class Meta:
        verbose_name = 'платеж'  # Настройка для наименования одного объекта
        verbose_name_plural = 'платежи'  # Настройка для наименования набора объектов
        ordering = ('id',)  # сортировка
