from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'phone_number', 'department', 'role', 'start_date', 'pay_per_event']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pay_per_event': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter pay per event'}),
        }
        labels = {
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'department': 'Department',
            'role': 'Role',
            'start_date': 'Date of Start',
            'pay_per_event': 'Pay Per Event',
        }
