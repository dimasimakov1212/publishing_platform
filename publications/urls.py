from django.urls import path


from publications.apps import PublicationsConfig
from publications.views import main_page_view, PublicationListView, PublicationCreateView, PublicationDetailView, \
    PublicationUpdateView, PublicationDeleteView

app_name = PublicationsConfig.name

urlpatterns = [
    path('', main_page_view, name='home'),
    path('publications/', PublicationListView.as_view(), name='publications_list'),
    path('create_publication/', PublicationCreateView.as_view(), name='create_publication'),
    path('publication/<int:pk>/', PublicationDetailView.as_view(), name='publication_detail'),
    path('publication_edit/<int:pk>/', PublicationUpdateView.as_view(), name='publication_edit'),
    path('publication_delete/<int:pk>/', PublicationDeleteView.as_view(), name='publication_delete'),
]
