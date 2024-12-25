from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from datetime import datetime

from .forms import EventForm
from .models import Event
from assignments.models import EmployeeAssignment, EventMaterialAllocation

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventForm

from django.db.models import F
from menu.models import Dish

from menu.models import Dish

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventForm
from menu.models import Dish  # Import Dish model


# Event List
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            selected_dishes_ids = request.POST.getlist('selected_dishes')
            selected_dishes = Dish.objects.filter(id__in=selected_dishes_ids)
            event.selected_dishes.set(selected_dishes)  
            messages.success(request, "Event added successfully!")
            return redirect('events:event_list')
    else:
        form = EventForm()

    # Fetch dishes grouped by their type
    dishes_by_category = {
        "Starters": Dish.objects.filter(dish_type='starter'),
        "First Main Dishes": Dish.objects.filter(dish_type='first_main'),
        "Second Main Dishes": Dish.objects.filter(dish_type='second_main'),
        "Desserts": Dish.objects.filter(dish_type='dessert'),
    }

    return render(request, 'events/event_form.html', {
        'form': form,
        'dishes_by_category': dishes_by_category,
    })

# Edit Event
def edit_event(request, pk):
    """
    Edit an existing event.
    """
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            # Update selected dishes
            selected_dishes_ids = request.POST.getlist('selected_dishes')
            selected_dishes = Dish.objects.filter(id__in=selected_dishes_ids)
            event.selected_dishes.set(selected_dishes)  # Update the dishes for the event
            messages.success(request, "Event updated successfully!")
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)

    # Group dishes by type
    dishes_by_category = {
        "Starters": Dish.objects.filter(dish_type='starter'),
        "First Main Dishes": Dish.objects.filter(dish_type='first_main'),
        "Second Main Dishes": Dish.objects.filter(dish_type='second_main'),
        "Desserts": Dish.objects.filter(dish_type='dessert'),
    }

    # Pre-select dishes for the event
    selected_dish_ids = event.selected_dishes.values_list('id', flat=True)

    return render(request, 'events/event_form.html', {
        'form': form,
        'dishes_by_category': dishes_by_category,
        'selected_dish_ids': selected_dish_ids,
    })

# Delete Event
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('events:event_list')
    return render(request, 'events/delete_confirmation.html', {'object': event})

# Event Calendar View
def event_calendar(request):
    return render(request, 'events/event_calendar.html')

# Calendar Events JSON
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

# Event Detail
def event_detail(request, event_id):
    """
    Display detailed information about a specific event, including selected dishes, assignments, and materials.
    """
    event = get_object_or_404(Event, pk=event_id)
    assignments = EmployeeAssignment.objects.filter(event=event)
    material_allocations = EventMaterialAllocation.objects.filter(event=event)
    selected_dishes = event.selected_dishes.all()  # Fetch the dishes selected for this event

    return render(request, 'events/event_detail.html', {
        'event': event,
        'assignments': assignments,
        'material_allocations': material_allocations,
        'selected_dishes': selected_dishes,  # Pass the selected dishes to the template
    })

# Event PDF Generation
def event_pdf(request, event_id):
    """
    Generate a PDF report for a specific event, including selected dishes, client, menu, assignments, and materials.
    """
    event = get_object_or_404(Event, id=event_id)
    assigned_employees = EmployeeAssignment.objects.filter(event=event)
    allocated_materials = EventMaterialAllocation.objects.filter(event=event)
    selected_dishes = event.selected_dishes.all()  # Include selected dishes in the PDF

    context = {
        'event': event,
        'client': event.client,
        'selected_dishes': selected_dishes,  # Add selected dishes to the context
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