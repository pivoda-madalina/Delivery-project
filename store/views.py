from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Restaurant, Category, Product
from django.urls import reverse_lazy, reverse
from .forms import ProductForm
from datetime import datetime
from .filters import RestaurantFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


class IndexView(ListView):
    model = Restaurant
    template_name = 'store/index.html'
    context_object_name = 'restaurants'

    def get_queryset(self):
        return Restaurant.objects.all()


class RestaurantList(ListView):
    model = Restaurant
    template_name = 'store/home.html'
    context_object_name = 'restaurants'

    def get_queryset(self):
        current_time = datetime.now().time()
        restaurants = Restaurant.objects.filter(opening_from__lte=current_time, opening_to__gt=current_time)
        return restaurants

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RestaurantList, self).get_context_data(**kwargs)
        my_filter = RestaurantFilter(self.request.GET, context.get('restaurants'))
        context['restaurants'] = my_filter.qs
        context['my_filter'] = my_filter
        return context


class DetailRestaurant(DetailView):
    model = Restaurant
    context_object_name = 'restaurant'
    template_name = 'store/detail_restaurant.html'

    def get_context_data(self, **kwargs):
        context = super(DetailRestaurant, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context


class AddRestaurant(CreateView):
    model = Restaurant
    template_name = 'store/add_restaurant.html'
    success_url = reverse_lazy('store:home')
    fields = '__all__'


class UpdateRestaurant(UpdateView):
    model = Restaurant
    template_name = 'store/update_restaurant.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('store:detail_restaurant', args=(self.object.id,))


class DeleteRestaurant(DeleteView):
    model = Restaurant
    template_name = 'store/delete_restaurant.html'
    context_object_name = 'restaurant'
    success_url = reverse_lazy('store:home')


class CategoryList(ListView):
    model = Category
    template_name = 'store/detail_restaurant.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


def add_category_for_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    category_id = request.POST.get('category_id')
    category = Category.objects.get(pk=category_id)
    restaurant.categories.add(category)
    return HttpResponseRedirect(reverse('store:detail_restaurant', args=(restaurant_id,)))


class AddCategory(CreateView):
    model = Category
    template_name = 'store/add_category.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('store:detail_restaurant', args=(self.kwargs.get('restaurant_id'),))


class ProductList(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs.get('category_id'))
        restaurant = Restaurant.objects.get(pk=self.kwargs.get('restaurant_id'))
        return Product.objects.filter(category=category, restaurant=restaurant)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('category_id')
        context['restaurant_id'] = self.kwargs.get('restaurant_id')
        return context


def show_products(request, restaurant_id, category_id):
    category = Category.objects.get(pk=category_id)
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    context = {'products': Product.objects.filter(category=category, restaurant__in=[restaurant]),
               'category_id': category_id,
               'restaurant_id': restaurant_id}
    return render(request, 'store/product_list.html', context)


def add_product(request, restaurant_id, category_id):
    category = Category.objects.get(pk=category_id)
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    if request.method == 'GET':
        return render(request, 'store/create_product.html', context={'form': ProductForm()})
    else:
        product = Product(price=request.POST.get('price'), name=request.POST.get('name'),
                          description=request.POST.get('description'), category=category, restaurant=restaurant)
        product.save()
        return HttpResponseRedirect(reverse('store:product_list', args=(restaurant_id, category_id)))


class AddProduct(CreateView):
    model = Product
    template_name = 'store/add_product.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('store:product_list', args=(self.kwargs.get('restaurant_id'),
                                                   self.kwargs.get('category_id')))


class UpdateProduct(UpdateView):
    model = Product
    template_name = 'store/update_product.html'
    fields = ('name', 'description', 'price', 'picture')

    def get_success_url(self):
        return reverse('store:product_list', args=(self.kwargs.get('restaurant_id'),
                                                   self.kwargs.get('category_id')))


def update_product(request, restaurant_id, category_id, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'GET':
        return render(request, 'store/update_product.html', context={'form': ProductForm()})
    else:
        product.price = request.POST.get('price')
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.picture = request.POST.get('picture')
        product.save()
        return HttpResponseRedirect(reverse('store:product_list', args=(restaurant_id, category_id)))


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'store/delete_product.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('store:product_list', args=(self.kwargs.get('restaurant_id'),
                                                   self.kwargs.get('category_id')))


def search_restaurant(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        restaurants = Restaurant.objects.filter(name__contains=searched)
        return render(request, 'store/search_restaurant.html', {'searched': searched,
                                                                'restaurants': restaurants})
    else:
        return render(request, 'store/search_restaurant.html', {})
