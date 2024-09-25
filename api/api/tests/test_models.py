from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from api.exceptions import NotEnoughShares
from api.models import Order, Stock


class StockTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Stock.objects.create(name="ROCK", price="60.20")

    def test_stock_creation(self):
        stock = Stock.objects.get(name="ROCK")
        self.assertEquals(stock.name, "ROCK")
        self.assertEquals(stock.price, Decimal("60.20"))

    def test_stock_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Stock.objects.create(
                name="ROCK",
                price=18.50,
            )


class OrderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="trader",
            password="trader",
            email="trader@gmail.com",
        )
        Stock.objects.create(name="PAPR", price=12.50)

    def test_order_quantity_cant_be_zero(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(stock_id=1, user_id=1, quantity=0)

    def test_cant_sell_more_than_available_stocks(self):
        Order.objects.create(stock_id=1, user_id=1, quantity=10)
        with self.assertRaises(NotEnoughShares):
            Order.objects.create(stock_id=1, user_id=1, quantity=-12)
