from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'date', 'start_time', 'end_time', 'event_type', 'client',
            'number_of_guests', 'venue_name', 'venue_address', 'venue_contact',
            'menu', 'special_instructions', 'assigned_staff', 'decorations_required',
            'logistics_notes', 'price_per_table', 'number_of_tables',
            'price_of_decoration', 'price_of_extras', 'event_cost', 'amount_paid',
            'payment_status', 'event_status', 'event_notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logistics_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'event_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
