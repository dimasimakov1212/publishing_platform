from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.views import UserConfirmedView, UserConfirmationFailView, user_authentication, verify_view, \
    UserAlreadyExistView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('register/', user_authentication, name='register'),
    # path('code_entering/', UserConfirmEmailView.as_view(), name='code_entering'),
    path('code_entering/', verify_view, name='code_entering'),
    # path('email_confirmation_sent/', UserConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('user_confirmed/', UserConfirmedView.as_view(), name='user_confirmed'),
    path('user_confirmation_failed/', UserConfirmationFailView.as_view(), name='user_confirmation_failed'),
    path('user_already_exist/', UserAlreadyExistView.as_view(), name='user_already_exist'),
    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('user_list', UserListView.as_view(), name='user_list'),
    # path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
    # path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    ]
