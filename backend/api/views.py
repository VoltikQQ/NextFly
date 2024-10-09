from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

from api.paginations import ItemAPIPagination
from api.serializers import ItemSerializer, CategorySerializer, ReviewsSerializer, PaymentHistorySerializer
from api.permissions import IsOwnerOrReadOnly, IsLoginOrReadOnly, IsAdminOrReadOnly
from cart.models import PaymentHistory
from recommend.models import Reviews
from shop.models import Item, Category


class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemAPIPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,
                          IsAdminOrReadOnly, )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsLoginOrReadOnly, )

    def perform_create(self, serializer):
        item_id = self.request.data.get('item')
        item = get_object_or_404(Item, id=item_id)

        parent_id = self.request.data.get('parent')
        parent = None
        if parent_id:
            parent = get_object_or_404(Reviews, id=parent_id)

        serializer.save(user=self.request.user, item=item, parent=parent)


class PaymentHistoryViewSet(viewsets.ModelViewSet):
    queryset = PaymentHistory.objects.all()
    serializer_class = PaymentHistorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, )


def health(request):
    return JsonResponse({"status": 200})