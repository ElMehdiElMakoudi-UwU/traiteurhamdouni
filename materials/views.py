from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Material
from .forms import MaterialForm
from events.models import Event

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Material
from .forms import MaterialForm


def material_list(request):
    materials = Material.objects.all()
    return render(request, 'materials/material_list.html', {'materials': materials})


def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Material added successfully!")
            return redirect('materials:list')
    else:
        form = MaterialForm()
    return render(request, 'materials/material_form.html', {'form': form})


def edit_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, "Material updated successfully!")
            return redirect('materials:list')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'materials/material_form.html', {'form': form})


def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, "Material deleted successfully!")
        return redirect('materials:list')
    return render(request, 'materials/delete_confirmation.html', {'object': material})

# def allocate_material(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if request.method == 'POST':
#         form = MaterialAllocationForm(request.POST)
#         if form.is_valid():
#             allocation = form.save(commit=False)
#             allocation.event = event
#             if allocation.quantity_allocated > allocation.material.quantity_available():
#                 messages.error(request, f"Not enough {allocation.material.name} available.")
#             else:
#                 allocation.save()
#                 messages.success(request, f"{allocation.quantity_allocated} {allocation.material.name} allocated.")
#             return redirect('events:event_detail', event_id=event.id)
#     else:
#         form = MaterialAllocationForm()
#     materials = Material.objects.all()
#     for material in materials:
#         material.available_quantity = material.quantity_available()
#     return render(request, 'materials/allocate_material.html', {
#         'form': form,
#         'materials': materials,
#         'event': event,
#     })
