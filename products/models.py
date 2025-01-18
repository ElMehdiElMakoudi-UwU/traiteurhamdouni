from django.db import models
from events.models import Event  # Assuming events app already exists

class Product(models.Model):
    PRODUCT_TYPES = [
        ('sweet', 'Sucres'),
        ('salted', 'Sales'),
        ('cake', 'Tartes'),
        ('soire', 'Petit Soiree'),
    ]

    name = models.CharField(max_length=255, verbose_name="Product Name")
    type = models.CharField(max_length=50, choices=PRODUCT_TYPES, verbose_name="Product Type")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Purchase Price")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Selling Price")

    def __str__(self):
        return self.name

class EventProduct(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="event_products")
    quantity = models.PositiveIntegerField(verbose_name="Quantity Required")

    def __str__(self):
        return f"{self.product.name} for {self.event.name}"