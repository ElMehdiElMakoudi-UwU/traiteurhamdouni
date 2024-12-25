from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerForm
from .models import Customer

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
from django.shortcuts import render
from .models import Customer
from django.db.models import Q

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

from django.shortcuts import render, get_object_or_404
from .models import Customer

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


from datetime import datetime
from django.shortcuts import render
from events.models import Event

def home(request):
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Query events for the current month
    monthly_events_count = Event.objects.filter(date__year=current_year, date__month=current_month).count()

    return render(request, 'home.html', {
        'monthly_events_count': monthly_events_count,
    })
