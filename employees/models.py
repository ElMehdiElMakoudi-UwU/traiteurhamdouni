from django.db import models
from django.core.exceptions import ValidationError

# Departments and Roles
DEPARTMENTS = [
    ('decoration', 'Decoration'),
    ('cooking', 'Cooking'),
    ('service', 'Service'),
    ('logistics', 'Logistics'),
]

ROLES = [
    ('manager', 'Manager'),
    ('staff', 'Staff'),
    ('chef', 'Chef'),
]

class Employee(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    department = models.CharField(max_length=50, choices=DEPARTMENTS, verbose_name="Department")
    role = models.CharField(max_length=50, choices=ROLES, verbose_name="Role")
    start_date = models.DateField(verbose_name="Date of Start")
    pay_per_event = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pay Per Event")

    def clean(self):
        # Ensure at least one manager exists per department
        if self.role == 'manager':
            return

        if not Employee.objects.filter(department=self.department, role='manager').exists():
            raise ValidationError(
                f"Each department must have at least one manager. No manager found in the '{self.get_department_display()}' department."
            )

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()} - {self.get_department_display()})"
