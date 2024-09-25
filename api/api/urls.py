from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# isort: off
from api.views import (
    OrderViewSet,
    StockViewSet,
    InvestmentViewSet,
    UserViewSet,
    BatchOrderUploadViewset,
)

# isort: on

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"stocks", StockViewSet)
router.register(r"orders", OrderViewSet)
router.register(
    r"batch-order-upload", BatchOrderUploadViewset, basename="batch-order-upload"
)
router.register(r"investments", InvestmentViewSet, basename="investments")
urlpatterns = [
    path("", include(router.urls)),
    # path(
    #     "total_investment/<int:stock_id>/",
    #     TotalInvestmentView.as_view(),
    #     name="total-investment",
    # ),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
