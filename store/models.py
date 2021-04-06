from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.name}"


class Restaurant(models.Model):
    OPEN = 1
    CLOSED = 2

    OPENING_STATUS = (
        (OPEN, 'open'),
        (CLOSED, 'closed'),
    )

    RATING = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

    name = models.CharField(max_length=50, unique=True)
    opening_status = models.IntegerField(choices=OPENING_STATUS, default=OPEN)
    opening_from = models.TimeField()
    opening_to = models.TimeField()
    kitchen = models.CharField(max_length=50)
    time_of_delivery = models.IntegerField(blank=True, null=True)
    cost_of_delivery = models.IntegerField(blank=True, null=True)
    picture = models.CharField(max_length=500)
    rating = models.IntegerField(choices=RATING)
    categories = models.ManyToManyField(Category, related_name='category_list')

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'

    def __str__(self):
        return f"{self.name}, {self.time_of_delivery}, {self.cost_of_delivery}, {self.rating}"


# class Review(models.Model):
#     RATING = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
#     rating = models.IntegerField(choices=RATING)


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    picture = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="products")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f"{self.name}, {self.price}, category: {self.category}, {self.restaurant}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    def __str__(self):
        return f"Product {self.product}, {self.quantity}."

    def get_cost(self):
        return self.price * self.quantity


class ShoppingCart(models.Model):
    product_order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Product {self.product_order}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.objects.all())


class PlacedOrder(models.Model):
    STATUS = (('Placed', 'Placed'), ('In progress', 'In progress'), ('Delivered', 'Delivered'))
    status = models.CharField(max_length=50)
    # status_order = models.IntegerField(choices=STATUS)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer")
    courier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="courier")

    def __str__(self):
        return f"Order {self.id}: {self.status}."
