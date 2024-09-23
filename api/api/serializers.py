from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from api.models import Order, Stock


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = ['name', 'price']


class OrderSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['amount', 'created_at']



