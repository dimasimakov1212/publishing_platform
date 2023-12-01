from django.urls import path


from publications.apps import PublicationsConfig
from publications.views import main_page_view, PublicationListView, PublicationCreateView

app_name = PublicationsConfig.name

urlpatterns = [
    path('', main_page_view, name='home'),
    path('publications/', PublicationListView.as_view(), name='publications_list'),
    path('create_publication/', PublicationCreateView.as_view(), name='create_publication'),
]
