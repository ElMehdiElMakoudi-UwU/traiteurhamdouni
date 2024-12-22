from django import forms
from .models import EmployeeAssignment

class EmployeeAssignmentForm(forms.ModelForm):
    class Meta:
        model = EmployeeAssignment
        fields = ['employee', 'event', 'assigned_role']
