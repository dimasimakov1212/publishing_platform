from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import CreateCheckoutSessionView, SuccessView, CancelView, product_create_view, \
    ProductLandingPageView, stripe_webhook

app_name = PaymentsConfig.name

urlpatterns = [
    path('create_checkout_session/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('product_create/<int:pk>/', product_create_view, name='product_create'),
    path('landing/<int:pk>/', ProductLandingPageView.as_view(), name='landing'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('webhooks/stripe/', stripe_webhook, name='webhooks_stripe'),
    ]
