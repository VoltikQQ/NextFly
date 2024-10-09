import json

import stripe
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.contrib.sessions.backends.db import SessionStore

import pickle

from .models import PaymentHistory
from shop.models import Item
from .cart import Cart
from .forms import CartAddItemForm
from shop.utils import menu
from django.conf import settings

from .tasks import send_payment_confirmation

# from .tasks import send_payment_confirmation

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    form = CartAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=item, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    context = {
        'menu': menu,
        'cat_selected': None,
        'cart': cart,
        'title': 'Cart'
    }
    for item in cart:
        item['update_quantity_form'] = CartAddItemForm(initial={'quantity': item['quantity'], 'update': True})

    return render(request, 'cart/details.html', context=context)


class CreateStripeCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs["pk"])

        success_uri = request.build_absolute_uri(reverse('cart:success'))

        discount_amount = int(item.price) * int(item.discount) / 100
        new_price = (int(item.price) - discount_amount) * 100

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(new_price),
                        "product_data": {
                            "name": item.title,
                            "description": item.description,
                            #"images": [f"{settings.BACKEND_DOMAIN}/media/{item.photos.all().first.url}"]
                        },
                    },
                    "quantity": self.kwargs["quantity"],
                }
            ],
            metadata={"item_id": item.id, 'user_id': request.user.id},
            mode="payment",
            success_url=f"{success_uri}?item_id={item.id}",
            cancel_url=request.build_absolute_uri(reverse('cart:cancel')),
        )
        return redirect(checkout_session.url)


# stripe listen --forward-to localhost:8000/cart/webhooks/stripe
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Payment successful")

        # Add this
        session = event["data"]["object"]
        customer_email = session["customer_details"]["email"]
        item_id = session["metadata"]["item_id"]
        user_id = session["metadata"]["user_id"]
        item = get_object_or_404(Item, id=item_id)
        user = get_object_or_404(User, id=user_id)

        payment = PaymentHistory.objects.create(
            email=customer_email, item=item, user=user, payment_status="C"
        )

        send_payment_confirmation.delay(payment.id)

    return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = "cart/success.html"

    def get(self, request, *args, **kwargs):
        item_id = request.GET.get('item_id')
        cart = Cart(request)
        item = get_object_or_404(Item, id=item_id)
        cart.remove(item)

        return super().get(request, *args, **kwargs)


class CancelView(TemplateView):
    template_name = "cart/cancel.html"
