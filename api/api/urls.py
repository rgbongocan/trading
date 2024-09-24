from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import OrderViewSet, StockViewSet, TotalInvestmentView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'orders', OrderViewSet)
# router.register(r'total_investment', TotalInvestmentView.as_view(), basename='total-investment')

urlpatterns = [
    path('', include(router.urls)),
    path('total_investment/<int:stock_id>/', TotalInvestmentView.as_view(), name='total-investment'),
    # path('/total-investment/<int:stock_id>', TotalInvestmentView.as_view(), name="total-investment"),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]