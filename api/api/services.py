from django.db.models import F, Sum


def get_id_from_url(url: str) -> int:
    return int(url.rstrip("/").split("/")[-1])


def get_shares(user, stock) -> int:
    from api.models import Order

    orders = Order.objects.filter(user=user, stock=stock)
    shares = orders.aggregate(shares=Sum(F("quantity")))["shares"]
    return shares
