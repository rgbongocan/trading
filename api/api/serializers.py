from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer

from api.models import Stock


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = ['name', 'price']
