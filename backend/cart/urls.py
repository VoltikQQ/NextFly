from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path(
        "create-checkout-session/<int:pk>/<int:quantity>/",
        views.CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path('/webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('/success/', views.SuccessView.as_view(), name='success'),
    path('/cancel/', views.CancelView.as_view(), name='cancel'),
]
