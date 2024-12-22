from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'category', 'total_quantity', 'notes']

# class MaterialAllocationForm(forms.ModelForm):
#     class Meta:
#         model = MaterialAllocation
#         fields = ['material', 'event', 'quantity_allocated']
