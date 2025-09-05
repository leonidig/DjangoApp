from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ["name", "description", "price", "category"]


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)