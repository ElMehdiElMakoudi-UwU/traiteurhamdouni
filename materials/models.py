from django.db import models
from events.models import Event

class Material(models.Model):
    CATEGORY_CHOICES = [
        ('seating', 'Seating'),
        ('tables', 'Tables'),
        ('dinnerware', 'Dinnerware'),
        ('decorations', 'Decorations'),
        ('equipment', 'Equipment'),
    ]
    name = models.CharField(max_length=255, verbose_name="Material Name")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Category")
    total_quantity = models.PositiveIntegerField(verbose_name="Total Quantity")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")

    def quantity_available(self):
        allocated = self.allocations.filter(event__end_time__gte=models.F('event__start_time')).aggregate(
            total=models.Sum('quantity_allocated'))['total'] or 0
        return self.total_quantity - allocated

    def __str__(self):
        return f"{self.name} ({self.category})"
