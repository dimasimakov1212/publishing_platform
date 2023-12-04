import os
from random import randint
import requests
import json

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from payments.models import Payment
from publications.models import Publication
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


def user_set_subscription(request):
    """ Добавление подписки пользователя """

    user = request.user  # получаем текущего пользователя

    payment = Payment.objects.filter(payment_user=user).last()  # получаем последний платеж пользователя

    publication = Publication.objects.get(id=payment.payment_publication.id)  # получаем оплаченную публикацию

    user.user_subscriptions.add(publication)  # добавляем публикацию в подписки пользователя

    user.save()

    return redirect(reverse('publications:user_subscriptions_list'))
