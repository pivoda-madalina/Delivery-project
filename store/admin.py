from django.contrib import admin
from .models import Restaurant, Product, Category, ShoppingCart, Order, PlacedOrder

admin.site.register(Restaurant)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ShoppingCart)
admin.site.register(PlacedOrder)