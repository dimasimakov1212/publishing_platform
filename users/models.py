from django.contrib.auth.models import AbstractUser
from django.db import models

from publications.models import Publication


class User(AbstractUser):
    username = None
    VERSION_CHOICES = ((True, 'Действующий'), (False, 'Заблокирован'))

    user_email = models.EmailField(unique=True, verbose_name='почта')
    user_phone = models.CharField(max_length=12, verbose_name='телефон', blank=True, null=True)
    user_avatar = models.ImageField(upload_to='users/', default='users/Аватарка без фото.png',
                                    verbose_name='аватар', blank=True, null=True)
    user_city = models.CharField(max_length=100, verbose_name='город', blank=True, null=True)
    user_description = models.CharField(max_length=150, verbose_name='Краткое описание', blank=True, null=True)
    is_active = models.BooleanField(choices=VERSION_CHOICES, default=False, verbose_name='Статус пользователя')
    user_subscriptions = models.ManyToManyField(Publication, verbose_name='подписка на публикации',
                                                blank=True, null=True)

    USERNAME_FIELD = "user_email"
    REQUIRED_FIELDS = []

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.user_email}'

    class Meta:
        verbose_name = 'Пользователь'  # наименование одного объекта
        verbose_name_plural = 'Пользователи'  # наименование набора объектов
        ordering = ('id',)  # поле для сортировки
