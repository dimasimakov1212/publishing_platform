import os

from django.conf import settings
from django.shortcuts import render, get_object_or_404
import stripe
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from payments.models import Product, Payment
from publications.models import Publication

stripe_public_key = os.getenv('STRIPE_PUBLIC_KEY')
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class CreateCheckoutSessionView(View):
    """ Создаем сессию оплаты Stripe """

    def post(self, request, *args, **kwargs):

        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)

        YOUR_DOMAIN = "http://127.0.0.1:8000/payments"

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
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    template_name = "payments/success.html"


class CancelView(TemplateView):
    template_name = "payments/cancel.html"


def product_create_view(request, pk):
    """ Создание продукта для продажи через stripe """

    publication = get_object_or_404(Publication, pk=pk)  # получаем публикацию по переданному pk
    author = publication.publication_owner  # получаем владельца публикации

    # создаем объект Product для передачи в stripe
    product = Product.objects.create(
        product_name=publication.publication_title,
        product_price=publication.publication_price * 100  # преобразуем цену в центы
    )
    product.save()

    # создаем объект Payment для проверки оплаты
    payment = Payment.objects.create(
        payment_user=request.user,
        payment_publication=publication,
        payment_product=product
    )
    payment.save()

    context = {
        'title': 'Продукт',
        'title_2': 'подготовка к оформлению покупки',
        'publication': publication,
        'author': author.first_name,
        'product': product
    }

    return render(request, 'payments/product_create.html', context)


class ProductLandingPageView(TemplateView):
    template_name = "payments/landing.html"

    def get_context_data(self, **kwargs):

        pk = kwargs['pk']
        product = Product.objects.get(pk=pk)

        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": stripe_public_key
        })
        return context


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # проверяем завершение оплаты
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

    return HttpResponse(status=200)
