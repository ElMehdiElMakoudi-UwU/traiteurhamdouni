from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Reservation
from .forms import ReservationForm

from django.db.models.functions import ExtractMonth, ExtractDay

def reservation_list(request):
    # Get the sorting parameter from the query string (default: ascending by date)
    sort = request.GET.get('sort', 'asc')
    toggle_sort = 'desc' if sort == 'asc' else 'asc'  # Determine the toggle direction

    # Get filters for day and month from the query string
    filter_day = request.GET.get('day')
    filter_month = request.GET.get('month')

    # Base query for reservations
    reservations = Reservation.objects.all()

    # Apply sorting
    if sort == 'desc':
        reservations = reservations.order_by('-date')
    else:
        reservations = reservations.order_by('date')

    # Apply filters for day and month
    if filter_day:
        reservations = reservations.annotate(day=ExtractDay('date')).filter(day=filter_day)
    if filter_month:
        reservations = reservations.annotate(month=ExtractMonth('date')).filter(month=filter_month)

    return render(request, 'reservations/reservation_list.html', {
        'reservations': reservations,
        'sort': sort,
        'toggle_sort': toggle_sort,
        'filter_day': filter_day,  # Pass current day filter to the template
        'filter_month': filter_month,  # Pass current month filter to the template
    })


def reservation_form(request, reservation_id=None):
    if reservation_id:
        reservation = get_object_or_404(Reservation, pk=reservation_id)
    else:
        reservation = None

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation saved successfully!")
            return redirect('reservations:reservation_list')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservations/reservation_form.html', {'form': form})

from django.http import JsonResponse
from .models import Reservation

def reservation_calendar_events(request):
    reservations = Reservation.objects.all()
    events = [
        {
            "title": f"{reservation.name} - {'Traiteur' if reservation.traiteur_required else 'No Traiteur'}",
            "start": str(reservation.date),
            "description": reservation.notes or "No notes",
        }
        for reservation in reservations
    ]
    return JsonResponse(events, safe=False)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Reservation

def delete_reservation(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.delete()
        messages.success(request, "Reservation deleted successfully!")
        return redirect('reservations:reservation_list')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('reservations:reservation_list')
