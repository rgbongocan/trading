from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from api.models import Stock
from api.serializers import StockSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]