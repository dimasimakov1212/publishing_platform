from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView

from users.forms import UserRegisterForm, UserEnterCodeForm
from users.models import User
from users.services import code_generator, users_list


class RegisterView(CreateView):
    """
    Регистрация нового пользователя и его валидация через письмо на email пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy('publications:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.last()
        context['user_pk'] = user.id

        print(context['user_pk'])

        return context

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.verify_code = code_generator()
        user.save()

        users_list()

        return redirect('users:code_entering')


class UserConfirmEmailView(TemplateView):
    """
    Подтверждение пользователем регистрации
    """
    form_class = UserEnterCodeForm
    template_name = "users/code_entering.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_list = RegisterView.as_view()(self.request)
        context['user_pk'] = my_list.context_data['user_pk']
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Your code here
        # Here request.POST is the same as self.request.POST
        # You can also access all possible self variables
        # like changing the template name for instance
        code = self.request.POST.get('verify_code', None)

        if code:
            pk = context['user_pk']
            user = User.objects.get(pk=pk)

            user_code = user.verify_code

            if code == user_code:
                user.is_active = True
                user.save()
                login(request, user)

                return redirect('users:email_confirmed')


class UserConfirmationSentView(PasswordResetDoneView):
    """
    Выводит информацию об отправке на почту подтверждения регистрации
    """
    template_name = "users/registration_sent_done.html"


class UserConfirmedView(TemplateView):
    """
    Выводит информацию об успешной регистрации пользователя
    """
    template_name = 'users/registration_confirmed.html'
