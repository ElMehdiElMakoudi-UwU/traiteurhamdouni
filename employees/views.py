from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError  # Add this line
from .forms import EmployeeForm
from .models import Employee

# List Employees
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

# Add New Employee
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Employee added successfully!")
                return redirect('employees:employee_list')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})

# Edit Existing Employee
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Employee updated successfully!")
                return redirect('employees:employee_list')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})

# Delete Employee
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect('employees:employee_list')
    return render(request, 'employees/delete_confirmation.html', {'object': employee})
