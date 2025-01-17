from django.urls import path
from .views import reservation_list, reservation_form, reservation_calendar_events, delete_reservation

app_name = 'reservations'

urlpatterns = [
    path('', reservation_list, name='reservation_list'),
    path('add/', reservation_form, name='add_reservation'),
    path('edit/<int:reservation_id>/', reservation_form, name='edit_reservation'),
    path('delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('calendar-events/', reservation_calendar_events, name='reservation_calendar_events'),
]
