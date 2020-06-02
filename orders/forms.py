from django import forms
from .models import Order

class CheckoutProductForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
