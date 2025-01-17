from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerForm
from .models import Customer
from django.shortcuts import render
from .models import Customer
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Customer
from datetime import datetime
from django.shortcuts import render
from events.models import Event
from django.db.models import Sum

# Add Customer View (already implemented)
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'client/add_customer.html', {'form': form})

# List Customers View (already implemented)
def customer_list(request):
    search_query = request.GET.get('q', '')  # Get the search query from the URL parameters
    sort_by = request.GET.get('sort_by', 'full_name')  # Default sort by 'full_name'
    order = request.GET.get('order', 'asc')  # Default order is 'asc'

    if order == 'desc':
        sort_by = f'-{sort_by}'

    # Filter customers based on the search query
    customers = Customer.objects.filter(
        Q(full_name__icontains=search_query) |
        Q(phone_number__icontains=search_query) |
        Q(address__icontains=search_query)
    ).order_by(sort_by)

    return render(request, 'client/customer_list.html', {
        'customers': customers,
        'current_sort': sort_by.lstrip('-'),
        'current_order': order,
        'search_query': search_query  # Pass the search query to the template
    })

# Edit Customer View
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'client/edit_customer.html', {'form': form, 'customer': customer})

# Delete Customer View
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'client/delete_customer.html', {'customer': customer})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    # Add logs or related data here if needed, for now, just the customer details
    activity_logs = [
        {"date": "2024-12-01", "action": "Added customer."},
        {"date": "2024-12-03", "action": "Updated address."},
    ]  # Example logs for demonstration

    return render(request, 'client/customer_detail.html', {
        'customer': customer,
        'activity_logs': activity_logs,
    })

from datetime import datetime, timedelta
from django.db.models import Sum, F
from events.models import Event
from reservation.models import Reservation

def home(request):
    now = datetime.now()
    today = now.date()

    # Calculate total revenue for all events in the current month
    total_revenue = (
        Event.objects.filter(date__year=now.year, date__month=now.month)
        .aggregate(total_revenue=Sum('event_cost'))['total_revenue']
    ) or 0

    # Get the count of events in the current month
    monthly_events_count = Event.objects.filter(date__year=now.year, date__month=now.month).count()

    # Find the next upcoming event
    next_event = Event.objects.filter(date__gte=today).order_by('date').first()
    days_until_next_event = (next_event.date - today).days if next_event else None

    # Calculate the count of reservations in the current month
    monthly_reservations_count = Reservation.objects.filter(date__year=now.year, date__month=now.month).count()

    # Find the next upcoming reservation
    next_reservation = Reservation.objects.filter(date__gte=today).order_by('date').first()
    days_until_next_reservation = (next_reservation.date - today).days if next_reservation else None

    # Calculate average revenue per event
    average_revenue_per_event = total_revenue / monthly_events_count if monthly_events_count > 0 else 0

    # Calculate percentage of booked days (events + reservations)
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    booked_days_count = (
        Event.objects.filter(date__month=now.month).values('date').distinct().count() +
        Reservation.objects.filter(date__month=now.month).values('date').distinct().count()
    )
    percentage_booked_days = (booked_days_count / end_of_month.day) * 100

    return render(request, 'home.html', {
        'total_revenue': total_revenue,
        'monthly_events_count': monthly_events_count,
        'next_event': next_event,
        'days_until_next_event': days_until_next_event,
        'monthly_reservations_count': monthly_reservations_count,
        'next_reservation': next_reservation,
        'days_until_next_reservation': days_until_next_reservation,
        'average_revenue_per_event': average_revenue_per_event,
        'percentage_booked_days': percentage_booked_days,
    })
