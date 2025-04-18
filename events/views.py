from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from datetime import datetime, date
from django.db.models import Q, Count, Sum, F, ExpressionWrapper, DecimalField
from .forms import EventForm
from .models import Event, EventProduct
from menu.models import Dish
from products.models import Product, EventProduct
from materials.models import Material
from employees.models import Employee
from assignments.models import EmployeeAssignment, EventMaterialAllocation
from reservation.models import Reservation


from django.db.models import Q

def event_list(request):
    query = request.GET.get('q', '')  # Get search query from the request
    events = Event.objects.all()

    if query:
        events = events.filter(
            Q(name__icontains=query) |  # Search by event name
            Q(event_type__icontains=query) |  # Search by event type
            Q(client__full_name__icontains=query)  # Correct field name for Customer
        )

    return render(request, 'events/event_list.html', {'events': events, 'query': query})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Save event data without committing to process related fields
            event = form.save(commit=False)
            event.event_cost = event.calculate_total_price()
            event.save()

            # Save selected dishes
            selected_dishes_ids = request.POST.getlist('selected_dishes')
            selected_dishes = Dish.objects.filter(id__in=selected_dishes_ids)
            event.selected_dishes.set(selected_dishes)

            # Save selected products and calculate their quantities
            selected_products_ids = request.POST.getlist('products')
            selected_products = Product.objects.filter(id__in=selected_products_ids)
            EventProduct.objects.filter(event=event).delete()  # Clear existing products for this event
            for product in selected_products:
                product_quantity = event.number_of_tables * 10  # Example calculation
                EventProduct.objects.create(event=event, product=product, quantity=product_quantity)

            # Save assigned employees
            employee_ids = request.POST.getlist('employees')
            assigned_role = request.POST.get('assigned_role', 'Staff')  # Default to 'Staff' role
            for employee_id in employee_ids:
                employee = get_object_or_404(Employee, pk=employee_id)
                EmployeeAssignment.objects.get_or_create(
                    employee=employee,
                    event=event,
                    defaults={'assigned_role': assigned_role}
                )

            # Save material allocations
            materials = Material.objects.all()
            for material in materials:
                quantity_allocated = int(request.POST.get(f'material_quantity_{material.id}', 0))
                if quantity_allocated > 0:
                    EventMaterialAllocation.objects.update_or_create(
                        event=event,
                        material=material,
                        defaults={'quantity_allocated': quantity_allocated}
                    )

            messages.success(request, "Event added successfully!")
            return redirect('events:event_list')
        else:
            messages.error(request, "There was an error adding the event.")
    else:
        form = EventForm()

    # Fetch dishes grouped by their type
    dishes_by_category = {
        "Starters": Dish.objects.filter(dish_type='starter'),
        "First Main Dishes": Dish.objects.filter(dish_type='first_main'),
        "Second Main Dishes": Dish.objects.filter(dish_type='second_main'),
        "Desserts": Dish.objects.filter(dish_type='dessert'),
    }

    # Fetch all available products grouped by category
    products_by_category = {
        "Sweets": Product.objects.filter(type="sweet"),
        "Salted": Product.objects.filter(type="salted"),
        "Cakes": Product.objects.filter(type="cake"),
        "Soirée Items": Product.objects.filter(type="soire"),
    }

    # Fetch employees
    employees = Employee.objects.all()

    # Fetch materials and initialize preselected materials dictionary
    materials = Material.objects.all()
    preselected_materials = {}

    return render(request, 'events/event_form.html', {
        'form': form,
        'dishes_by_category': dishes_by_category,
        'products_by_category': products_by_category,
        'employees': employees,  # Pass employees to the template
        'materials': materials,  # Pass materials to the template
        'preselected_materials': preselected_materials,  # Preselected materials (empty on add)
    })

def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            # Save updated event details
            event = form.save(commit=False)
            event.event_cost = event.calculate_total_price()
            event.save()

            # Update selected dishes
            selected_dishes_ids = request.POST.getlist('selected_dishes')
            selected_dishes = Dish.objects.filter(id__in=selected_dishes_ids)
            event.selected_dishes.set(selected_dishes)

            # Update selected products
            selected_products_ids = request.POST.getlist('products')
            selected_products = Product.objects.filter(id__in=selected_products_ids)
            EventProduct.objects.filter(event=event).delete()
            for product in selected_products:
                product_quantity = event.number_of_tables * 10
                EventProduct.objects.create(event=event, product=product, quantity=product_quantity)

            # Update materials allocation
            materials_ids = request.POST.getlist('materials')
            EventMaterialAllocation.objects.filter(event=event).delete()  # Clear previous allocations
            for material_id in materials_ids:
                quantity_allocated = int(request.POST.get(f'material_quantity_{material_id}', 0))
                if quantity_allocated > 0:
                    EventMaterialAllocation.objects.create(
                        material_id=material_id,
                        event=event,
                        quantity_allocated=quantity_allocated,
                    )

            # Update employee assignments
            employee_ids = request.POST.getlist('employees')
            EmployeeAssignment.objects.filter(event=event).delete()  # Clear previous assignments
            assigned_role = request.POST.get('assigned_role', 'Staff')
            for employee_id in employee_ids:
                EmployeeAssignment.objects.get_or_create(
                    employee_id=employee_id,
                    event=event,
                    defaults={'assigned_role': assigned_role},
                )

            messages.success(request, "Event updated successfully!")
            return redirect('events:event_detail', event_id=event.id)
        else:
            messages.error(request, "There was an error updating the event.")
    else:
        form = EventForm(instance=event)

    # Prepare context data
    dishes_by_category = {
        "Starters": Dish.objects.filter(dish_type='starter'),
        "First Main Dishes": Dish.objects.filter(dish_type='first_main'),
        "Second Main Dishes": Dish.objects.filter(dish_type='second_main'),
        "Desserts": Dish.objects.filter(dish_type='dessert'),
    }

    products_by_category = {
        "Sweets": Product.objects.filter(type="sweet"),
        "Salted": Product.objects.filter(type="salted"),
        "Cakes": Product.objects.filter(type="cake"),
        "Soirée Items": Product.objects.filter(type="soire"),
    }

    materials = Material.objects.all()
    employees = Employee.objects.all()

    # Preselect data for the form
    preselected_dishes = event.selected_dishes.values_list('id', flat=True)
    preselected_products = EventProduct.objects.filter(event=event).values_list('product_id', flat=True)
    preselected_materials = {
        allocation['material_id']: allocation['quantity_allocated']
        for allocation in EventMaterialAllocation.objects.filter(event=event).values('material_id', 'quantity_allocated')
    }
    preselected_employees = EmployeeAssignment.objects.filter(event=event).values_list('employee_id', flat=True)

    return render(request, 'events/event_form.html', {
        'form': form,
        'dishes_by_category': dishes_by_category,
        'products_by_category': products_by_category,
        'materials': materials,
        'employees': employees,
        'event': event,
        'preselected_dishes': preselected_dishes,
        'preselected_products': preselected_products,
        'preselected_materials': preselected_materials,
        'preselected_employees': preselected_employees,
    })

def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('events:event_list')
    return render(request, 'events/delete_confirmation.html', {'object': event})

def event_calendar(request):
    return render(request, 'events/event_calendar.html')

def calendar_events(request):
    events = Event.objects.all()
    event_data = [
        {
            'title': event.name,
            'start': event.date.isoformat(),
            'url': f"/events/{event.id}/",  # Link to event detail
        }
        for event in events
    ]
    return JsonResponse(event_data, safe=False)

def event_detail(request, event_id):
    """
    Display detailed information about a specific event, including selected dishes, assignments, materials, and products.
    """
    event = get_object_or_404(Event, pk=event_id)
    assignments = EmployeeAssignment.objects.filter(event=event)
    material_allocations = EventMaterialAllocation.objects.filter(event=event)
    selected_dishes = event.selected_dishes.all()
    event_products = EventProduct.objects.filter(event=event)  # Fetch associated products and quantities

    return render(request, 'events/event_detail.html', {
        'event': event,
        'assignments': assignments,
        'material_allocations': material_allocations,
        'selected_dishes': selected_dishes,
        'event_products': event_products,  # Include event products in the context
    })

def event_pdf(request, event_id):
    """
    Generate a PDF report for a specific event, including selected dishes, products, client, menu, assignments, and materials.
    """
    event = get_object_or_404(Event, id=event_id)
    assigned_employees = EmployeeAssignment.objects.filter(event=event)
    allocated_materials = EventMaterialAllocation.objects.filter(event=event)
    selected_dishes = event.selected_dishes.all()
    event_products = EventProduct.objects.filter(event=event)  # Include products in the PDF

    context = {
        'event': event,
        'client': event.client,
        'selected_dishes': selected_dishes,
        'event_products': event_products,  # Add products to the context
        'assignments': assigned_employees,
        'allocated_materials': allocated_materials,
        'current_year': datetime.now().year,
    }

    template = get_template('events/event_pdf.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="event_{event.id}_details.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def dashboard(request):
    # Metrics
    total_events = Event.objects.count()
    total_reservations = Reservation.objects.count()
    total_revenue = Reservation.objects.aggregate(total=Sum('total_amount'))['total'] or 0

    # Calculate pending payments dynamically
    reservations_with_pending = Reservation.objects.annotate(
        remaining_amount=ExpressionWrapper(
            F('total_amount') - F('advance_amount'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )
    total_pending_payments = reservations_with_pending.aggregate(
        pending=Sum('remaining_amount')
    )['pending'] or 0

    total_employees_assigned = EmployeeAssignment.objects.values('employee').distinct().count()

    # Upcoming Events
    upcoming_events = Event.objects.filter(date__gte=date.today()).order_by('date')[:5]

    # Popular Materials
    popular_materials = Material.objects.annotate(
        total_allocated=Sum('allocations__quantity_allocated')
    ).order_by('-total_allocated')[:5]

    context = {
        'total_events': total_events,
        'total_reservations': total_reservations,
        'total_revenue': total_revenue,
        'total_pending_payments': total_pending_payments,
        'total_employees_assigned': total_employees_assigned,
        'upcoming_events': upcoming_events,
        'popular_materials': popular_materials,
    }
    return render(request, 'events/dashboard.html', context)
