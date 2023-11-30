from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    """ Форма регистрации пользователя """
    user_phone = forms.CharField(help_text='Номер телефона в формате +70000000000')
    class Meta:
        model = User
        fields = ('user_phone', 'user_email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserEnterCodeForm(forms.ModelForm):
    """ Форма для ввода кода подтверждения """
    verify_code = forms.CharField(label='Регистрация', help_text='Код подтверждения')

    class Meta:
        model = User
        fields = ('verify_code',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(UserChangeForm):
    """ Форма редактирования профиля пользователя """

    class Meta:
        model = User
        fields = ('user_email', 'first_name', 'last_name', 'user_phone', 'user_city', 'user_avatar', 'user_description')

    def __init__(self, *args, **kwargs):
        """ Дополнительные настройки """
        super().__init__(*args, **kwargs)

        # Позволяет не выводить в профиле поле пароля
        self.fields['password'].widget = forms.HiddenInput()

        # передаем в шаблон контроль формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
