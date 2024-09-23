from django.db.models import CharField, DecimalField, Model


class Stock(Model):
    name = CharField(max_length=100, unique=True)
    price = DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name