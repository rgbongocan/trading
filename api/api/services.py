from django.contrib.auth.models import User
from django.db.models import F, Sum

from api.models import Order, Stock


def get_id_from_url(url: str) -> int:
    return url.rstrip('/').split('/')[-1]


def get_shares(user: User, stock: Stock):
    orders = Order.objects.filter(user=user, stock=stock)
    shares = orders.aggregate(
        shares=Sum(F('amount'))
    )['shares']
    return shares