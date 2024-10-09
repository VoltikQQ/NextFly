from rest_framework import routers

from .views import *

item_router = routers.DefaultRouter()
item_router.register(r'items', ItemsViewSet)

cat_router = routers.DefaultRouter()
cat_router.register(r'category', CategoryViewSet)

rev_router = routers.DefaultRouter()
rev_router.register(r'reviews', ReviewsViewSet)

payment_router = routers.DefaultRouter()
payment_router.register(r'payment-history', PaymentHistoryViewSet)