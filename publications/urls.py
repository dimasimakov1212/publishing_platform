from django.urls import path


from publications.apps import PublicationsConfig
from publications.views import main_page_view

app_name = PublicationsConfig.name

urlpatterns = [
    path('', main_page_view, name='home'),
]
