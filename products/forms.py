from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type', 'purchase_price', 'selling_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
