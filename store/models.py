from django.db import models
from datetime import datetime


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

    @property
    def opening_status(self):
        current_time = datetime.now().time()
        if self.opening_from <= current_time < self.opening_to:
            return 'open'
        return 'closed'


class Review(models.Model):
    RATING = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    rating = models.IntegerField(choices=RATING)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}"


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
