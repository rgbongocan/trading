import pandas as pd
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.models import Order, Stock

# isort: off
from api.serializers import (
    BatchOrderUploadSerializer,
    OrderSerializer,
    StockSerializer,
    UserSerializer,
)

# isort: on
from api.services import get_shares

UserModel = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user).all()
        return Response(
            OrderSerializer(orders, many=True, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )


class BatchOrderUploadViewset(ViewSet):
    EXPECTED_COLUMNS = {"stock", "quantity"}
    permission_classes = [IsAuthenticated]
    serializer_class = BatchOrderUploadSerializer

    def create(self, request):
        file = request.FILES.get("file")
        if not file:
            raise ValidationError("File upload is required")
        df_orders = pd.read_csv(file)
        if set(df_orders.columns) != self.EXPECTED_COLUMNS:
            raise ValidationError("Only columns allowed are: stock, quantity")
        try:
            with transaction.atomic():
                for idx, row in df_orders.iterrows():
                    user = self.request.user
                    stock = Stock.objects.get(name=row["stock"])
                    order = Order(user=user, stock=stock, quantity=row["quantity"])
                    # we opt for individual object creation instead
                    # of bulk_create to trigger validations
                    order.save()
        except Stock.DoesNotExist:
            raise ValidationError("Invalid stock name encountered")
        return Response(
            {"message": f"{len(df_orders.index)} orders successfully executed"},
            status=status.HTTP_201_CREATED,
        )


class InvestmentViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = self.request.user
        stocks_with_total_quantity = (
            Stock.objects.filter(order__user=user)
            .annotate(
                shares=Sum("order__quantity"),
                value=ExpressionWrapper(
                    Sum("order__quantity") * F("price"), output_field=DecimalField()
                ),
            )
            .all()
        )
        # could have a dedicated serializer for the response
        return Response(
            {
                "investments": [
                    {
                        "url": request.build_absolute_uri(
                            reverse("investments-detail", kwargs={"pk": s.id})
                        ),
                        "name": s.name,
                        "price": s.price,
                        "shares": s.shares,
                        "value": s.value,
                    }
                    for s in stocks_with_total_quantity
                ]
            },
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        user = self.request.user
        stock = Stock.objects.get(pk=pk)
        shares = get_shares(user, stock)
        return Response(
            {
                "shares": shares,
                "shares_value": shares * stock.price,
                "stock": StockSerializer(stock, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )
