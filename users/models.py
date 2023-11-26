from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    VERSION_CHOICES = ((True, 'Действующий'), (False, 'Заблокирован'))

    user_email = models.EmailField(unique=True, verbose_name='почта')
    user_phone = models.CharField(max_length=12, verbose_name='телефон', blank=True, null=True)
    user_avatar = models.ImageField(upload_to='media/users/', default='/media/users/Аватарка без фото.png',
                                    verbose_name='аватар', blank=True, null=True)
    user_city = models.CharField(max_length=100, verbose_name='город', blank=True, null=True)
    is_active = models.BooleanField(choices=VERSION_CHOICES, default=True, verbose_name='Статус пользователя')
    verify_code = models.CharField(max_length=4, verbose_name='код верификации', blank=True, null=True)

    USERNAME_FIELD = "user_email"
    REQUIRED_FIELDS = []

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.user_email}'

    class Meta:
        verbose_name = 'Пользователь'  # наименование одного объекта
        verbose_name_plural = 'Пользователи'  # наименование набора объектов
        ordering = ('id',)  # поле для сортировки
