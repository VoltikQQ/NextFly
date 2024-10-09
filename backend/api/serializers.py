from rest_framework import serializers
from django.contrib.auth import get_user_model

from cart.models import PaymentHistory
from recommend.models import Reviews
from shop.models import Item, Category

User = get_user_model()


class ItemSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.SlugRelatedField(
        many=False,
        slug_field="name",
        queryset=Category.objects.all()
    )
    total_rating = serializers.HiddenField(default=0)
    num_rating = serializers.HiddenField(default=0)
    avg_rating = serializers.HiddenField(default=0)


    class Meta:
        model = Item
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = ['id', 'time_create']


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = '__all__'