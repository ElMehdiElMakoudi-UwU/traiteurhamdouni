from django.urls import path
from .views import employee_list, add_employee, edit_employee, delete_employee

app_name = 'employees'  # Namespace for the app

urlpatterns = [
    path('', employee_list, name='employee_list'),  # List all employees
    path('add/', add_employee, name='add_employee'),  # Add a new employee
    path('edit/<int:pk>/', edit_employee, name='edit_employee'),  # Edit an existing employee
    path('delete/<int:pk>/', delete_employee, name='delete_employee'),  # Delete an employee
]
