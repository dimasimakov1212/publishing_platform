from django.db import models

from config import settings


class Publication(models.Model):
    """ Модель публикации """

    VERSION_CHOICES = ((True, 'Публичная'), (False, 'Приватная'))

    publication_title = models.CharField(max_length=200, verbose_name='заголовок публикации', blank=True, null=True)
    publication_text = models.TextField(verbose_name='содержание публикации', blank=True, null=True)
    publication_photo = models.ImageField(upload_to='publications/', verbose_name='заставка', blank=True, null=True)
    is_public = models.BooleanField(choices=VERSION_CHOICES, default=True, verbose_name='статус публикации')
    publication_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена публикации')
    publication_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.publication_title}'

    class Meta:
        verbose_name = 'публикация'  # наименование одного объекта
        verbose_name_plural = 'публикации'  # наименование набора объектов
        ordering = ('id',)  # поле для сортировки
