from django.conf import settings
from django.db import transaction

from api.exceptions import NotEnoughShares
from api.services import get_shares

# isort: off
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    Model,
)

# isort: on


class Stock(Model):
    name = CharField(max_length=100, unique=True)
    # we store price as a decimal with 2 decimal places
    price = DecimalField(
        max_digits=10, decimal_places=2, help_text="Decimal with two places"
    )

    def __str__(self):
        return self.name


class Order(Model):
    # TODO: rename amount to quantity
    amount = IntegerField(help_text="Negative for a sell order")
    stock = ForeignKey(Stock, on_delete=CASCADE)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    @property
    def value(self):
        return f"{self.amount * self.stock.price}¤"

    def __str__(self):
        action = "bought" if self.amount > 0 else "sold"
        return f"{self.user.username} {action} {self.amount} units of {self.stock.name}"

    @transaction.atomic()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_shares = get_shares(self.user, self.stock)
        if self.amount < 0 and total_shares < 0:
            raise NotEnoughShares("Not enough shares to sell")
