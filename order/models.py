from django.db import models
from store.models import Product
from django.conf import settings


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Product {self.product}, {self.quantity}."

    def get_cost(self):
        self.product_total_cost = self.product.price * self.quantity
        return self.product_total_cost


class ShoppingCart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f"Product {self.orders}."

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.orders.all())


class PlacedOrder(models.Model):
    STATUS = (('Placed', 'Placed'), ('In progress', 'In progress'), ('Delivered', 'Delivered'))
    status = models.IntegerField(choices=STATUS)
    created_on = models.DateTimeField(auto_now_add=True)
    orders = models.ManyToManyField(Order)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer")
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="courier",
                                default=None, null=True)

    def __str__(self):
        return f"Order {self.id}: {self.status}."
