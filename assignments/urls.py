from django.urls import path
from .views import fetch_employee_availability, assign_employee, fetch_roles, unassign_employee, bulk_allocate_materials

app_name = 'assignments'

urlpatterns = [
    path('assign/', assign_employee, name='assign_employee'),
    path('fetch-availability/', fetch_employee_availability, name='fetch_availability'),
    path('fetch-roles/', fetch_roles, name='fetch_roles'),
    path('unassign/<int:assignment_id>/', unassign_employee, name='unassign_employee'),
    path('bulk-allocate/<int:event_id>/', bulk_allocate_materials, name='bulk_allocate_materials'),
]
