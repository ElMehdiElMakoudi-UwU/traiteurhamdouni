from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=255, verbose_name="Client Name")
    date = models.DateField(verbose_name="Reservation Date")
    decorations_required = models.BooleanField(default=False, verbose_name="Decorations Required")
    traiteur_required = models.BooleanField(default=False, verbose_name="Traiteur Required")
    traiteur_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Caterer Name")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Advance Amount")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")

    @property
    def remaining_amount(self):
        return self.total_amount - self.advance_amount

    def __str__(self):
        return f"{self.name} - {self.date}"
