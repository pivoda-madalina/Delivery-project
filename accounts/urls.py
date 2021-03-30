from django.urls import path
from .views import LoginCustomView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginCustomView.as_view(), name='login'),
]
