from django import forms
from .models import Dish, Menu

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'dish_type', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dish name'}),
            'dish_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
        }


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'starter_dish', 'first_main_plate', 'second_main_plate', 'dessert']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter menu name'}),
            'starter_dish': forms.Select(attrs={'class': 'form-select'}),
            'first_main_plate': forms.Select(attrs={'class': 'form-select'}),
            'second_main_plate': forms.Select(attrs={'class': 'form-select'}),
            'dessert': forms.Select(attrs={'class': 'form-select'}),
        }
