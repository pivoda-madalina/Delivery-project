from .models import Order
from django.forms import ModelForm
from store.models import Product
from bootstrap_modal_forms.forms import BSModalModelForm


class OrderModelForm(BSModalModelForm):
    class Meta:
        model = Order
        fields = ['quantity']

