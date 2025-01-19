from django import forms
from .models import Event
from menu.models import Dish


from django import forms
from .models import Event
from menu.models import Dish
from products.models import Product
from employees.models import Employee
from materials.models import Material

class EventForm(forms.ModelForm):
    selected_dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Select Dishes",
    )
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Select Products"
    )
    assigned_employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Assign Employees"
    )
    assigned_materials = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Assign Materials"
    )


    class Meta:
        model = Event
        fields = [
            'name', 'date', 'start_time', 'end_time', 'event_type', 'client',
            'number_of_guests', 'venue_name', 'venue_address', 'venue_contact',
            'assigned_staff', 'decorations_required',
            'logistics_notes', 'price_per_table', 'number_of_tables',
            'price_of_decoration', 'price_of_extras', 'event_cost', 'amount_paid',
            'payment_status', 'event_status', 'event_notes', 'selected_dishes', 'products','assigned_employees', 'assigned_materials',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'logistics_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'event_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

from django import forms
from products.models import Product
from events.models import EventProduct


class EventProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = EventProduct
        fields = ['product', 'quantity']
