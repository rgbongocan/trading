from django.contrib import admin
from django.contrib.auth.models import User

# from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from api.models import Order, Stock
from api.serializers import OrderSerializer, StockSerializer, UserSerializer


# move to views.py
class UserViewSet(ModelViewSet):
    # todo: change to get_user_model?
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]