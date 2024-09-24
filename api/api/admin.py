from django.contrib import admin

from api.models import Order, Stock

admin.site.register(Stock)
admin.site.register(Order)
