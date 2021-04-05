from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    start_program = models.IntegerField(blank=True, null=True)
    end_program = models.IntegerField(blank=True, null=True)
    kitchen = models.CharField(max_length=50)
    time_of_delivery = models.IntegerField(blank=True, null=True)
    cost_of_delivery = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.name}, {self.time_of_delivery}, {self.cost_of_delivery}, {self.rating}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="products")
    restaurant = models.ManyToManyField(Restaurant)

    def __str__(self):
        return f"{self.name}, {self.price}, category: {self.category}, {self.restaurant}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    product_number = models.IntegerField()

    def __str__(self):
        return f"Product {self.product}, {self.product_number}"


class ShoppingCart(models.Model):
    product_order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Product {self.product_order}"


class PlacedOrder(models.Model):
    status = models.CharField(max_length=50)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer")
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="courier")

    def __str__(self):
        return f"Order {self.id}: {self.status}."
