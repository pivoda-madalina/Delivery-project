from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model
from django.contrib.auth.models import AbstractUser


choises = (('Client', 'Client'), ('Restaurant', 'Restaurant'), ('Delivery', 'Delivery'))


class CustomUser(AbstractUser):
    user_type = models.CharField(choices=choises, max_length=50)
    address = models.CharField(max_length=500, null=True, blank=True)
    picture = models.CharField(max_length=500, null=True, blank=True)
    accept_terms = models.BooleanField(default=False)
