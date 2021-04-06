from django.urls import path
from .views import RestaurantList, DetailRestaurant, AddRestaurant, UpdateRestaurant, DeleteRestaurant, \
    AddCategory, show_products, AddProduct, add_category_for_restaurant, add_product, UpdateProduct, update_product, \
    DeleteProduct, ProductList

app_name = 'store'
urlpatterns = [
    path('', RestaurantList.as_view(), name='home'),
    path('<int:pk>', DetailRestaurant.as_view(), name='detail_restaurant'),
    path('create_restaurant', AddRestaurant.as_view(), name='add_restaurant'),
    path('update_restaurant/<int:pk>', UpdateRestaurant.as_view(), name='update_restaurant'),
    path('delete_restaurant/<int:pk>', DeleteRestaurant.as_view(), name='delete_restaurant'),
    path('detail_restaurant/<int:restaurant_id>/category/<int:category_id>', ProductList.as_view(),
         name='product_list'),
    path('detail_restaurant/<int:restaurant_id>', add_category_for_restaurant, name='add_category'),
    path('detail_restaurant/<int:restaurant_id>/category/<int:category_id>/create_product', add_product,
         name='add_product'),
    path('detail_restaurant/<int:restaurant_id>/category/<int:category_id>/update_product/<int:pk>',
         UpdateProduct.as_view(), name='update_product'),
    path('detail_restaurant/<int:restaurant_id>/category/<int:category_id>/delete_product/<int:pk>',
         DeleteProduct.as_view(), name='delete_product'),

]
