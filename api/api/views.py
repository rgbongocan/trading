from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Order, Stock
from api.serializers import OrderSerializer, StockSerializer, UserSerializer

UserModel = get_user_model()

class UserViewSet(ModelViewSet):
    # permission class is superuser
    # todo: change to get_user_model?
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class StockViewSet(ModelViewSet):
    # create endpoint should be for admin
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # todo: only show user's orders
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # TODO: logic to only sell if you have enough bought
        return super(OrderViewSet, self).create(request, *args, **kwargs)


class TotalInvestmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, stock_id, *args, **kwargs):
        print(args, kwargs)
        user = self.request.user
        stock = Stock.objects.get(pk=stock_id)
        qs = Order.objects.filter(user=user, stock=stock)
        total_amount = qs.aggregate(
            total_amount=Sum(F('amount'))
        )['total_amount']
        return Response({
            'total_amount': total_amount,
            'total_value': total_amount * stock.price,
            'stock': StockSerializer(stock, context={'request': request}).data,
        }, status=status.HTTP_200_OK)



# class PlaceOrderView(APIView):
#     serializer_class = OrderSerializer
#     permissions_classes = [IsAuthenticated]
#     http_method_names = ['delete']
#     # renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         print(data)
#         return Response({}, status=status.HTTP_200_OK)