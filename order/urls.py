from django.urls import path
from .views import OrderView, ShoppingCartView, UpdateOrderView, DeleteOrderView, OrderHistoryView, submit_order, \
    take_order, delete_view

app_name = 'order'
urlpatterns = [
    path('detail_restaurant/<int:restaurant_id>/category/<int:category_id>/order/<int:pk>', OrderView.as_view(),
         name='order_view'),
    path('shopping_cart/<int:pk>', ShoppingCartView.as_view(), name='shopping_cart'),
    path('update_order/<int:pk>', UpdateOrderView.as_view(), name='update_order'),
    path('delete_order/<int:pk>', DeleteOrderView.as_view(),
         name='delete_order'),
    path('submit_order', submit_order, name='submit_order'),
    path('orderhistory', OrderHistoryView.as_view(), name='order_history'),
    path('take_order/<int:placed_order_id>', take_order, name='take_order'),
    path('delete_history', delete_view, name='clear_history')
]
