from django import forms
from .models import Event
from menu.models import Dish


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'date', 'start_time', 'end_time', 'event_type', 'client',
            'number_of_guests', 'venue_name', 'venue_address', 'venue_contact',
            'assigned_staff', 'decorations_required',
            'logistics_notes', 'price_per_table', 'number_of_tables',
            'price_of_decoration', 'price_of_extras', 'event_cost', 'amount_paid',
            'payment_status', 'event_status', 'event_notes', 'selected_dishes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'logistics_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'event_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    selected_dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Dishes",
    )
