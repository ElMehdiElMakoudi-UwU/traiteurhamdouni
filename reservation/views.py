from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Reservation
from .forms import ReservationForm

def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})

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
    """
    Provide reservation data for the calendar in JSON format.
    """
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
