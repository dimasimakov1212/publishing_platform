from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm


class RegisterView(CreateView):
    """
    Регистрация нового пользователя и его валидация через письмо на email пользователя
    """
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy('publications:home')

    def get_context_data(self, **kwargs):
        """ Выводит контекстную информацию в шаблон """
        context = super(RegisterView, self).get_context_data(**kwargs)

        context['title'] = 'Регистрация'
        context['title_2'] = 'регистрация пользователя'

        return context

    # def form_valid(self, form):
    #     user = form.save()
    #     user.is_active = False
    #     user.save()
    #
    #     # формируем токен и ссылку для подтверждения регистрации
    #     token = default_token_generator.make_token(user)
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
    #
    #     current_site = '127.0.0.1:8000'
    #
    #     send_mail(
    #         subject='Регистрация на платформе',
    #         message=f"Завершите регистрацию, перейдя по ссылке: http://{current_site}{activation_url}",
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[user.email]
    #     )
    #     return redirect('publications/homepage.html')
