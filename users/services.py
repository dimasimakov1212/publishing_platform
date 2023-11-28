import os
from random import randint
import requests
import json

from users.models import User


def code_generator():
    """ Генератор кода для регистрации пользователя """

    code = str(randint(1000, 9999))

    return code


def users_list():

    users = User.objects.all()

    for user in users:
        print(f"{user.id} - {user.user_email}")


def send_sms(sms_text, user_phone):
    """ Отправка смс-сообщения """

    api_key = os.getenv('SMS_PROSTO_API_KEY')  # получаем API ключ
    text = sms_text  # текст сообщения
    phone = user_phone  # телефон пользователя

    # формируем адрес запроса через API
    url_api = (f'https://ssl.bs00.ru/'
               f'?method=push_msg&format=json&key={api_key}&text={text}&phone={phone}&sender_name=P-platform')

    req = requests.get(url_api)  # Посылаем запрос по API

    if req.status_code == 200:  # проверяем на корректность ответа

        data_in = req.content.decode()  # Декодируем ответ API, чтобы Кириллица отображалась корректно
        req.close()

        data_json = json.dumps(data_in)  # загружаем данные в формате json
        data_out = json.loads(data_json)  # преобразуем полученные данные из формата json
        print(data_out)

    if req.status_code != 200:
        print("В настоящий момент отправка смс невозможна. Попробуйте позже.")
