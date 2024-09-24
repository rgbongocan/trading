from django.contrib.auth.models import User
from rest_framework.serializers import DecimalField, HyperlinkedModelSerializer

from api.models import Order, Stock


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class StockSerializer(HyperlinkedModelSerializer):
    # create endpoint should be for admin
    # price = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Stock
        fields = ['url', 'name', 'price']


class OrderSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'amount', 'created_at', 'user', 'stock']



