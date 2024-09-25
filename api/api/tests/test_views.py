from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import Order, Stock
from api.services import get_id_from_url, get_shares


class OrderViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stock_rock = Stock.objects.create(name="ROCK", price="80.00")
        cls.stock_xsor = Stock.objects.create(name="XSOR", price="60.20")
        cls.user_bob = User.objects.create_user(
            username="bob",
            password="newport",
            email="bob@yahoo.com",
        )
        cls.user_alice = User.objects.create_user(
            username="alice",
            password="gander",
            email="alice@gmail.com",
        )
        cls.client = APIClient()
        cls.bob_rock_order1 = Order.objects.create(
            user=cls.user_bob,
            stock=cls.stock_rock,
            quantity=2.5,
        )
        Order.objects.create(
            user=cls.user_alice,
            stock=cls.stock_xsor,
            quantity=3.1,
        )
        Order.objects.create(
            user=cls.user_bob,
            stock=cls.stock_xsor,
            quantity=3,
        )
        cls.bob_rock_order2 = Order.objects.create(
            user=cls.user_bob,
            stock=cls.stock_rock,
            quantity=13.0,
        )

    def test_only_own_orders(self):
        self.client.login(username="bob", password="newport")
        response = self.client.get(reverse("order-list"))
        self.assertEquals(response.status_code, 200)

        response_order_ids = {get_id_from_url(order["url"]) for order in response.data}
        self.assertSetEqual(
            response_order_ids,
            set(Order.objects.filter(user=self.user_bob).values_list("id", flat=True)),
        )

    def test_shares_aggregation(self):
        shares = get_shares(self.user_bob, self.stock_rock)
        self.assertEquals(
            shares, self.bob_rock_order1.quantity + self.bob_rock_order2.quantity
        )

    def test_investment_value(self):
        self.client.login(username="bob", password="newport")
        response = self.client.get(
            reverse("investments-detail", kwargs={"pk": self.stock_rock.id})
        )
        self.assertEquals(
            response.data["shares_value"],
            Decimal(self.stock_rock.price) * get_shares(self.user_bob, self.stock_rock),
        )
