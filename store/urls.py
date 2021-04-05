from django.urls import path
from .views import homepage

app_name = 'store'
urlpatterns = [
    path('', homepage, name='home'),
]
