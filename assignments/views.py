from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import EmployeeAssignment
from .forms import EmployeeAssignmentForm
from employees.models import Employee
from events.models import Event


def assign_employee_page(request):
    events = Event.objects.all()
    return render(request, 'assignments/assign_employee.html', {'events': events})

def fetch_roles(request):
    department = request.GET.get('department')
    if not department:
        return JsonResponse({'roles': []})  # Return an empty list if no department is selected

    roles = Employee.objects.filter(department=department).values_list('role', flat=True).distinct()
    return JsonResponse({'roles': list(roles)})

def assign_employee(request):
    employees = Employee.objects.all()
    events = Event.objects.all()
    event_id = request.GET.get('event_id')
    event = get_object_or_404(Event, pk=event_id) if event_id else None

    if request.method == 'POST':
        # Handle bulk assignment
        employee_ids = request.POST.getlist('employees')  # Get selected employee IDs
        assigned_role = request.POST.get('assigned_role', 'Staff')  # Get selected role
        event_id = request.POST.get('event')  # Get event ID from form
        event = get_object_or_404(Event, pk=event_id)

        if employee_ids:
            for employee_id in employee_ids:
                employee = get_object_or_404(Employee, pk=employee_id)
                EmployeeAssignment.objects.get_or_create(
                    employee=employee,
                    event=event,
                    defaults={'assigned_role': assigned_role}  # Use the selected role
                )
            messages.success(request, "Employees assigned successfully!")
        else:
            messages.warning(request, "No employees selected for assignment.")

        return redirect(f"/assignments/assign/?event_id={event.id}")

    # Fetch availability logic (same as before)
    availability = []
    for employee in employees:
        current_event_assignment = EmployeeAssignment.objects.filter(employee=employee, event=event).first()

        if current_event_assignment:
            availability.append({
                'id': employee.id,
                'name': employee.full_name,
                'status': 'Taken',
                'assigned_event': event.name,
            })
        else:
            overlapping_assignment = (
                EmployeeAssignment.objects
                .filter(employee=employee)
                .filter(event__date=event.date)
                .filter(
                    event__start_time__lt=event.end_time,
                    event__end_time__gt=event.start_time
                )
                .first()
            )
            if overlapping_assignment:
                availability.append({
                    'id': employee.id,
                    'name': employee.full_name,
                    'status': 'Taken',
                    'assigned_event': overlapping_assignment.event.name,
                })
            else:
                availability.append({
                    'id': employee.id,
                    'name': employee.full_name,
                    'status': 'Free',
                    'assigned_event': None,
                })

    return render(request, 'assignments/assign_employee.html', {
        'events': events,
        'availability': availability,
        'event': event,
    })

def view_assignments(request, event_id):
    assignments = EmployeeAssignment.objects.filter(event_id=event_id)
    return render(request, 'assignments/view_assignments.html', {'assignments': assignments})

def employee_availability(request):
    assignments = EmployeeAssignment.objects.select_related('event').all()
    return render(request, 'assignments/employee_availability.html', {'assignments': assignments})

def fetch_employee_availability(request):
    event_id = request.GET.get('event_id')

    if not event_id:
        return JsonResponse({'error': 'Event ID not provided'}, status=400)

    event = Event.objects.filter(pk=event_id).first()
    if not event:
        return JsonResponse({'error': 'Invalid Event ID'}, status=404)

    employees = Employee.objects.all()
    availability = []

    for employee in employees:
        current_event_assignment = EmployeeAssignment.objects.filter(employee=employee, event=event).first()

        if current_event_assignment:
            availability.append({
                'id': employee.id,
                'name': employee.full_name,
                'department': employee.department,
                'role': employee.role,
                'status': 'Taken',
                'assigned_event': event.name,
            })
        else:
            overlapping_assignment = EmployeeAssignment.objects.filter(
                employee=employee,
                event__date=event.date,
            ).exclude(event=event).first()

            if overlapping_assignment:
                availability.append({
                    'id': employee.id,
                    'name': employee.full_name,
                    'department': employee.department,
                    'role': employee.role,
                    'status': 'Taken',
                    'assigned_event': overlapping_assignment.event.name,
                })
            else:
                availability.append({
                    'id': employee.id,
                    'name': employee.full_name,
                    'department': employee.department,
                    'role': employee.role,
                    'status': 'Free',
                    'assigned_event': None,
                })

    return JsonResponse({'availability': availability})

def unassign_employee(request, assignment_id):
    assignment = get_object_or_404(EmployeeAssignment, pk=assignment_id)

    if request.method == 'POST':
        assignment.delete()
        messages.success(request, f"Employee '{assignment.employee.full_name}' has been unassigned from the event.")
        return redirect('events:event_detail', event_id=assignment.event.id)

# assignments/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from materials.models import Material
from events.models import Event
from .models import EventMaterialAllocation
from django.db import models


def bulk_allocate_materials(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    materials = Material.objects.all()

    # Calculate dynamic availability
    for material in materials:
        allocated = material.allocations.filter(event__date=event.date).aggregate(total=models.Sum('quantity_allocated'))['total'] or 0
        material.available_quantity = material.total_quantity - allocated

    if request.method == 'POST':
        for material in materials:
            quantity = int(request.POST.get(f'quantity_{material.id}', 0))
            if quantity > 0:
                if quantity > material.available_quantity:
                    messages.error(request, f"Not enough {material.name} available.")
                    return redirect('assignments:bulk_allocate_materials', event_id=event.id)

                EventMaterialAllocation.objects.create(material=material, event=event, quantity_allocated=quantity)

        messages.success(request, "Materials allocated successfully.")
        return redirect('events:event_detail', event_id=event.id)

    return render(request, 'assignments/bulk_allocate_materials.html', {
        'event': event,
        'materials': materials,
    })
