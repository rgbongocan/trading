import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import F, Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Order, Stock
from api.serializers import OrderSerializer, StockSerializer, UserSerializer
from api.services import get_id_from_url, get_shares

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
        data = self.request.data
        amount = int(data.get('amount'))
        stock_url = data.get('stock')
        stock_id = get_id_from_url(stock_url)
        stock = Stock.objects.get(pk=stock_id)
        if amount < 0:
            shares = get_shares(self.request.user, stock)
            if amount + shares < 0:
                raise PermissionDenied("You do not have enough shares to sell.")
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
            OrderSerializer(orders, many=True, context={'request': request}).data,
            status=status.HTTP_200_OK
        )


# consider putting under order viewset?
class TotalInvestmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, stock_id, *args, **kwargs):
        print(args, kwargs)
        user = self.request.user
        stock = Stock.objects.get(pk=stock_id)
        shares = get_shares(user, stock)
        return Response({
            'shares': shares,
            'shares_value': shares * stock.price,
            'stock': StockSerializer(stock, context={'request': request}).data,
        }, status=status.HTTP_200_OK)

