from django.db import models


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
