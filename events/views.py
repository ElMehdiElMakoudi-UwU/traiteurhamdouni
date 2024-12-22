from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from datetime import datetime

from .forms import EventForm
from .models import Event
from assignments.models import EmployeeAssignment, EventMaterialAllocation

# Event List
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

# Add Event
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, "Event added successfully!")
            return redirect('events:event_list')
        else:
            print("Form is invalid", form.errors)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

# Edit Event
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('events:event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

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
    event = get_object_or_404(Event, pk=event_id)
    assignments = EmployeeAssignment.objects.filter(event=event)
    material_allocations = EventMaterialAllocation.objects.filter(event=event)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'assignments': assignments,
        'material_allocations': material_allocations,
    })

# Event PDF Generation
def event_pdf(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    assigned_employees = EmployeeAssignment.objects.filter(event=event)
    allocated_materials = EventMaterialAllocation.objects.filter(event=event)

    context = {
        'event': event,
        'client': event.client,
        'menu': event.menu,
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
