from django.core.management import BaseCommand
import os

from users.models import User

SUPER_USER_PASSWORD = os.getenv('SUPER_USER_PASSWORD')


class Command(BaseCommand):
    """ Создание суперпользователя """

    def handle(self, *args, **options):
        user = User.objects.create(
            user_email='admin@dima.pro',
            first_name='Admin',
            last_name='Dima',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        user.set_password(SUPER_USER_PASSWORD)
        user.save()
