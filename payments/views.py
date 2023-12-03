import os

from django.shortcuts import render
import stripe
from django.http import JsonResponse
from django.views import View

from payments.models import Product

public_token = os.getenv('STRIPE_PUBLIC_KEY')
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class CreateCheckoutSessionView(View):
    """ Создаем сессию оплаты Stripe """

    def post(self, request, *args, **kwargs):

        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)

        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.product_price,
                        'product_data': {
                            'name': product.product_name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
