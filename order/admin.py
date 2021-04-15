from django.contrib import admin
from .models import Order, ShoppingCart, PlacedOrder

admin.site.register(Order)
admin.site.register(ShoppingCart)
admin.site.register(PlacedOrder)
