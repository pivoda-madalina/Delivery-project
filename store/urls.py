from django.urls import path
from .views import homepage

app_name = 'accounts'
urlpatterns = [
    path('', homepage, name='home'),
]