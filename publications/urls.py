from django.urls import path


from publications.apps import PublicationsConfig
from publications.views import main_page_view, UserPublicationListView, PublicationCreateView, PublicationDetailView, \
    PublicationUpdateView, PublicationDeleteView, other_users_page_view, OtherUserPublicationListView, \
    user_subscriptions_view, FinishSubscriptionView, contacts_view

app_name = PublicationsConfig.name

urlpatterns = [
    path('', main_page_view, name='home'),
    path('publications/', other_users_page_view, name='publications_list'),
    path('user_publications/', UserPublicationListView.as_view(), name='user_publications_list'),
    path('other_user_publications/<int:pk>/', OtherUserPublicationListView.as_view(), name='other_user_publications'),
    path('create_publication/', PublicationCreateView.as_view(), name='create_publication'),
    path('publication/<int:pk>/', PublicationDetailView.as_view(), name='publication_detail'),
    path('publication_edit/<int:pk>/', PublicationUpdateView.as_view(), name='publication_edit'),
    path('publication_delete/<int:pk>/', PublicationDeleteView.as_view(), name='publication_delete'),
    path('user_subscriptions/', user_subscriptions_view, name='user_subscriptions_list'),
    path('finish_subscription/', FinishSubscriptionView.as_view(), name='finish_subscription'),
    path('contacts/', contacts_view, name='contacts'),
]
