from django.urls import path
from .views import event_list, add_event, edit_event, delete_event, event_calendar, calendar_events, event_detail, event_pdf, dashboard
app_name = 'events'

urlpatterns = [
    path('', event_list, name='event_list'),
    path('add/', add_event, name='add_event'),
    path('edit/<int:event_id>/', edit_event, name='edit_event'),
    path('delete/<int:pk>/', delete_event, name='delete_event'),
    path('calendar/', event_calendar, name='event_calendar'),
    path('calendar-events/', calendar_events, name='calendar_events'),
    path('<int:event_id>/', event_detail, name='event_detail'),  # View details of an event
    path('<int:event_id>/pdf/', event_pdf, name='event_pdf'),
    path('dashboard/', dashboard, name='dashboard'),
]
