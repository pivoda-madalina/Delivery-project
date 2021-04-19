from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from .models import Order, ShoppingCart, PlacedOrder
from store.models import Product
from .forms import OrderModelForm
from bootstrap_modal_forms.generic import BSModalCreateView


class OrderView(BSModalCreateView):
    model = Order
    template_name = 'order/order_view.html'
    context_object_name = 'order'
    form_class = OrderModelForm
    success_message = 'Success: Order was created.'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        context['product'] = product
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs.get('pk'))
        cart, _ = ShoppingCart.objects.get_or_create(user=self.request.user)
        form.instance.save()
        cart.orders.add(form.instance)
        return super(OrderView, self).form_valid(form)

    def get_success_url(self):
        return reverse('store:product_list', args=(self.kwargs.get('restaurant_id'),
                                                   self.kwargs.get('category_id')))


class ShoppingCartView(DetailView):
    model = ShoppingCart
    template_name = 'order/shopping_cart.html'
    context_object_name = 'cart'


class UpdateOrderView(UpdateView):
    model = Order
    template_name = 'order/update_order.html'
    fields = ('quantity',)
    # success_url = reverse_lazy('order:shopping_cart')

    def get_success_url(self):
        return reverse('order:shopping_cart', args=(self.object.user.shoppingcart.id,))


class DeleteOrderView(DeleteView):
    model = Order
    template_name = 'order/delete_order.html'
    context_object_name = 'order'
    # success_url = reverse_lazy('order:shopping_cart')

    def get_success_url(self):
        return reverse('order:shopping_cart', args=(self.object.user.shoppingcart.id,))


def submit_order(request):
    shopping_cart = request.user.shoppingcart
    submitted_order = PlacedOrder.objects.create(status=1, customer=request.user)
    if not shopping_cart.orders.count():
        return render(request, 'order/shopping_cart.html', {'error_message': 'Cart is empty!'})
    else:
        for order in shopping_cart.orders.all():
            submitted_order.orders.add(order)
            shopping_cart.orders.remove(order)
    return HttpResponseRedirect(reverse('order:order_history'))


class OrderHistoryView(ListView):
    model = PlacedOrder
    template_name = 'order/orderhistory.html'
    context_object_name = 'orders'
    queryset = PlacedOrder.objects.all()


def take_order(request, placed_order_id):
    submitted_order = PlacedOrder.objects.get(pk=placed_order_id)
    if submitted_order.status == 1:
        submitted_order.status = 2
    elif submitted_order.status == 2:
        submitted_order.status = 3
    submitted_order.save()
    return HttpResponseRedirect(reverse('order:order_history'))
