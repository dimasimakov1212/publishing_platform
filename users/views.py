from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetDoneView
from django.db import IntegrityError
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserEnterCodeForm, UserProfileForm
from users.models import User
from users.services import code_generator, users_list, send_sms


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

    form = UserRegisterForm(request.POST)  # класс-метод формы регистрации
    data = {'form': form, 'title': 'Регистрация'}  # контекстная информация

    try:
        # получаем данные пользователя
        if request.method == 'POST':

            if form.is_valid():
                user = form.save()
                user.set_password(form.cleaned_data['password1'])
                user.save()

                users_list()

                # получаем случайно сгенерированный код и записываем его в кэш сессии
                request.session['verify_code'] = code_generator()

                if user is not None:
                    request.session['pk'] = user.pk  # заносим в кэш сессии id текущего пользователя

                    return redirect('users:code_entering')  # перенаправляем на форму ввода кода верификации

    except IntegrityError:
        return redirect('users:user_already_exist')  # перенаправляем на форму, что пользователь уже существует

    return render(request, 'users/register.html', context=data)


def verify_view(request):
    """ Верификация пользователя через подтверждение кода верификации """

    form = UserEnterCodeForm  # класс-метод формы регистрации
    data = {'form': form, 'title': 'Подтверждение'}  # контекстная информация

    pk = request.session.get('pk')  # получаем из кэша сессии id текущего пользователя
    verify_code = request.session.get('verify_code')  # получаем из кэша сессии код верификации

    if pk:
        user = User.objects.get(pk=pk)  # получаем пользователя

        # отправка смс временно отключена, код выводится в терминале
        # send_sms(verify_code, user.user_phone) # отправляем смс с кодом верификации пользователю

        print(verify_code)

        if request.method == 'POST':

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

    return render(request, 'users/code_entering.html', context=data)


class ProfileView(UpdateView):
    """ Контроллер профиля пользователя """

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('publications:home')

    def get_object(self, queryset=None):
        """ Получаем текущего пользователя """
        return self.request.user

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """
        context = super(ProfileView, self).get_context_data(**kwargs)

        context['title'] = 'Профиль'
        context['title_2'] = 'редактирование профиля пользователя'

        return context


class UserListView(ListView):
    """ Выводит список пользователей """

    model = User
    # permission_required = 'users.view_user'
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """

        context = super(UserListView, self).get_context_data(**kwargs)

        context['title'] = 'Пользователи'
        context['title_2'] = 'интересное от наших пользователей'

        return context
