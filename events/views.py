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


from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import EventForm
from .models import Event, Dish
from products.models import Product
from products.models import EventProduct


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, EventProduct
from .forms import EventForm
from menu.models import Dish
from products.models import Product

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, EventProduct
from .forms import EventForm
from menu.models import Dish
from products.models import Product

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, EventProduct
from .forms import EventForm
from menu.models import Dish
from products.models import Product

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
                product_quantity = event.number_of_tables * 10  # Calculate quantity
                EventProduct.objects.create(event=event, product=product, quantity=product_quantity)

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

    return render(request, 'events/event_form.html', {
        'form': form,
        'dishes_by_category': dishes_by_category,
        'products_by_category': products_by_category,  # Pass grouped products to the template
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import EventForm
from menu.models import Dish
from products.models import Product, EventProduct


def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()

            # Update selected dishes
            selected_dishes_ids = request.POST.getlist("selected_dishes")
            selected_dishes = Dish.objects.filter(id__in=selected_dishes_ids)
            event.selected_dishes.set(selected_dishes)

            # Update selected products and quantities
            selected_products = request.POST.getlist("products")
            for product_id in selected_products:
                quantity = request.POST.get(f"quantity_{product_id}", 0)
                EventProduct.objects.update_or_create(
                    event=event,
                    product_id=product_id,
                    defaults={"quantity": quantity},
                )

            # Remove products that are no longer selected
            current_products = EventProduct.objects.filter(event=event)
            current_products.exclude(product_id__in=selected_products).delete()

            messages.success(request, "Event updated successfully!")
            return redirect("events:event_list")
        else:
            messages.error(request, "There was an error updating the event.")
    else:
        form = EventForm(instance=event)

    # Fetch dishes grouped by their type
    dishes_by_category = {
        "Starters": Dish.objects.filter(dish_type="starter"),
        "First Main Dishes": Dish.objects.filter(dish_type="first_main"),
        "Second Main Dishes": Dish.objects.filter(dish_type="second_main"),
        "Desserts": Dish.objects.filter(dish_type="dessert"),
    }

    # Fetch products grouped by their type
    products_by_category = {
        "Sweets": Product.objects.filter(type="sweet"),
        "Salted": Product.objects.filter(type="salted"),
        "Cakes": Product.objects.filter(type="cake"),
        "Soirée Items": Product.objects.filter(type="soire"),
    }

    # Preselected dishes
    preselected_dishes = list(event.selected_dishes.values_list("id", flat=True))

    # Preselected products and their quantities
    preselected_products = {
        ep.product_id: ep.quantity
        for ep in EventProduct.objects.filter(event=event)
    }

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "dishes_by_category": dishes_by_category,
            "products_by_category": products_by_category,
            "preselected_dishes": preselected_dishes,
            "preselected_products": preselected_products,
        },
    )


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