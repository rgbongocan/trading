from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    Model,
)


class Stock(Model):
    name = CharField(max_length=100, unique=True)
    price = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(Model):
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
