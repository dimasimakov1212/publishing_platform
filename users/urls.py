from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.services import user_set_subscription
from users.views import UserConfirmedView, UserConfirmationFailView, user_authentication, verify_view, \
    UserAlreadyExistView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', user_authentication, name='register'),
    path('code_entering/', verify_view, name='code_entering'),
    path('user_confirmed/', UserConfirmedView.as_view(), name='user_confirmed'),
    path('user_confirmation_failed/', UserConfirmationFailView.as_view(), name='user_confirmation_failed'),
    path('user_already_exist/', UserAlreadyExistView.as_view(), name='user_already_exist'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('set_subscription/', user_set_subscription, name='set_subscription'),
    ]
