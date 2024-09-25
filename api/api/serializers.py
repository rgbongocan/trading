from django.contrib.auth.models import User

from api.models import Order, Stock

# isort: off
from rest_framework.serializers import (
    FileField,
    HyperlinkedModelSerializer,
    Serializer,
)

# isort: on


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class StockSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ["url", "name", "price"]


class OrderSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ["url", "amount", "created_at", "stock"]


class BatchOrderUploadSerializer(Serializer):
    file = FileField(required=True)

    class Meta:
        fields = ["file"]
