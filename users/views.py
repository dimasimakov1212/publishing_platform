from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView
from django.db import IntegrityError
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView

from users.forms import UserRegisterForm, UserEnterCodeForm
from users.models import User
from users.services import code_generator, users_list


# ----------- регистрация и валидация нового пользователя сделана через функции -----------
# class RegisterView(CreateView):
#     """ Регистрация нового пользователя """
#
#     model = User
#     form_class = UserRegisterForm
#     template_name = "users/register.html"
#     success_url = reverse_lazy('publications:home')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = User.objects.last()
#         # user = self.request.user
#         # print(user)
#         context['user_pk'] = user.id
#
#         return context
#
#     def form_valid(self, form):
#         user = form.save()
#         user.is_active = False
#         user.verify_code = code_generator()
#         print(user.id)
#         user.save()
#
#         users_list()
#
#         return redirect('users:code_entering')
#
#
# class UserConfirmEmailView(TemplateView):
#     """
#     Подтверждение пользователем регистрации
#     """
#     form_class = UserEnterCodeForm
#     template_name = "users/code_entering.html"
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         my_list = RegisterView.as_view()(self.request)
#
#         context['user_pk'] = my_list.context_data['user_pk']
#         # print(context['user_pk'])
#         return context
#
#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#
#         # verify_code = code_generator()
#         # print(verify_code)
#
#         code = self.request.POST.get('verify_code', None)
#
#
#         if code:
#             pk = context['user_pk']
#             user = User.objects.get(pk=pk)
#
#             user_code = user.verify_code
#
#             if code == user_code:
#                 user.is_active = True
#                 user.save()
#                 login(request, user)
#
#                 return redirect('users:user_confirmed')
#
#             else:
#                 user.delete()
#                 return redirect('users:user_confirmation_failed')
# -------------------------- конец ---------------------------------------------


class UserConfirmationSentView(PasswordResetDoneView):
    """ Выводит информацию об отправке кода подтверждения по смс """

    template_name = "users/registration_sent_done.html"


class UserConfirmedView(TemplateView):
    """ Выводит информацию об успешной регистрации пользователя """

    template_name = 'users/user_confirmed.html'


class UserConfirmationFailView(TemplateView):
    """ Выводит информацию о невозможности зарегистрировать пользователя """

    template_name = 'users/user_confirmation_failed.html'


class UserAlreadyExistView(TemplateView):
    """ Выводит информацию, что пользователь с таким email уже существует """

    template_name = 'users/user_already_exist.html'


def user_authentication(request):
    """ Регистрация нового пользователя """

    form = UserRegisterForm  # класс-метод формы регистрации

    try:
        # получаем данные пользователя
        if request.method == 'POST':
            username = request.POST.get('user_email')
            user_email = request.POST.get('user_email')
            password = request.POST.get('password1')
            user_phone = request.POST.get('user_phone')

            # аутентификация пользователя
            user = authenticate(request, username=username, user_email=user_email, password=password,
                                user_phone=user_phone)
            # создаем объект пользователя
            user = User.objects.create(user_email=user_email, password=password, user_phone=user_phone)

            users_list()

            # получаем случайно сгенерированный код и записываем его в кэш сессии
            request.session['verify_code'] = code_generator()

            if user is not None:
                request.session['pk'] = user.pk  # заносим в кэш сессии id текущего пользователя

                return redirect('users:code_entering')  # перенаправляем на форму ввода кода верификации

    except IntegrityError:
        return redirect('users:user_already_exist')  # перенаправляем на форму, что пользователь уже существует

    return render(request, 'users/register.html', {'form': form})


def verify_view(request):
    """ Верификация пользователя через подтверждение кода верификации """

    form = UserEnterCodeForm  # класс-метод формы регистрации

    pk = request.session.get('pk')  # получаем из кэша сессии id текущего пользователя
    verify_code = request.session.get('verify_code')  # получаем из кэша сессии код верификации

    print(verify_code)

    if request.method == 'POST':
        if pk:
            user = User.objects.get(pk=pk)  # получаем пользователя

            code = request.POST.get('verify_code')  # получаем код введенный пользователем

            # если коды совпадают, активируем пользователя и логиним его в системе
            if code == verify_code:
                user.is_active = True
                user.save()
                login(request, user)

                return redirect('users:user_confirmed')  # выводим сообщение об успешной регистрации

            # если коды не совпадают, удаляем текущего пользователя из БД
            else:
                user.delete()
                return redirect('users:user_confirmation_failed')  # выводим сообщение об ошибке регистрации

    return render(request, 'users/code_entering.html', {'form': form})
