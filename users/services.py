from random import randint

from users.models import User


def code_generator():
    """ Генератор кода для регистрации пользователя """

    code = str(randint(1000, 9999))

    return code


def users_list():

    users = User.objects.all()

    for user in users:
        print(f"{user.id} - {user.user_email}")
