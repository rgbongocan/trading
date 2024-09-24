from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# isort: off
from api.views import (
    OrderViewSet,
    StockViewSet,
    TotalInvestmentView,
    UserViewSet,
)

# isort: on

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"stocks", StockViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "total_investment/<int:stock_id>/",
        TotalInvestmentView.as_view(),
        name="total-investment",
    ),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
