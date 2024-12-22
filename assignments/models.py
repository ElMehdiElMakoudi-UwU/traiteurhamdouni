from django.db import models
from employees.models import Employee
from events.models import Event
from django.core.exceptions import ValidationError
from datetime import datetime


class EmployeeAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assignments")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="assignments")
    assigned_role = models.CharField(max_length=50, verbose_name="Assigned Role", blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'event')  # Ensure an employee can't be assigned to the same event twice

    def clean(self):
        # Validation for double assignments during overlapping events
        overlapping_assignments = EmployeeAssignment.objects.filter(
            employee=self.employee,
            event__date=self.event.date,
        ).exclude(event=self.event)
        for assignment in overlapping_assignments:
            if (
                self.event.start_time < assignment.event.end_time
                and self.event.end_time > assignment.event.start_time
            ):
                raise ValidationError(f"{self.employee.full_name} is already assigned to another event during this time.")

    def __str__(self):
        return f"{self.employee.full_name} assigned to {self.event.name} as {self.assigned_role or 'Unknown Role'}"

# assignments/models.py

from django.db import models
from events.models import Event
from materials.models import Material

class EventMaterialAllocation(models.Model):  # Renamed from MaterialAllocation
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="material_allocations")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="allocations")
    quantity_allocated = models.PositiveIntegerField()
    date_allocated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity_allocated} {self.material.name} for {self.event.name}"
