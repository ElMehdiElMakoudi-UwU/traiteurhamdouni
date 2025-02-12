from django.db import models
from client.models import Customer
from menu.models import Dish
from employees.models import Employee

class Event(models.Model):
    EVENT_TYPES = [
        ('wedding', 'Mariage'),
        ('corporate', 'Événement d\'entreprise'),
        ('birthday', 'Anniversaire'),
        ('private', 'Fête privée'),
        ('engagement', 'Fiançailles'),
        ('baptism', 'Baptême'),
        ('marriage_signature', 'Signature d\'acte de mariage'),
        ('family_reunion', 'Réunion de famille'),
        ('conference', 'Conférence'),
        ('charity_event', 'Événement caritatif'),
        ('graduation', 'Remise de diplômes'),
        ('baby_shower', 'Fête de naissance'),
        ('festival', 'Festival'),
        ('exhibition', 'Exposition'),
        ('concert', 'Concert'),
        ('anniversary', 'Anniversaire de mariage'),
        ('new_year', 'Nouvel An'),
        ('retirement', 'Départ à la retraite'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('partial', 'Avance'),
        ('paid', 'Payé'),
    ]

    EVENT_STATUS_CHOICES = [
        ('scheduled', 'Programmé'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]

    # Basic Information
    name = models.CharField(max_length=255, verbose_name="Event Name")
    date = models.DateField(verbose_name="Event Date")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, blank=True, verbose_name="Event Type")

    # Client Information
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="events")
    number_of_guests = models.PositiveIntegerField(blank=True, null=True, verbose_name="Number of Guests")

    # Venue Information
    venue_name = models.CharField(max_length=255, blank=True, verbose_name="Venue Name")
    venue_address = models.TextField(blank=True, verbose_name="Venue Address")
    venue_contact = models.CharField(max_length=20, verbose_name="Venue Contact", blank=True, null=True)

    # Dish Selection (Instead of Menu)
    selected_dishes = models.ManyToManyField(Dish, related_name="events", verbose_name="Selected Dishes")

    # Product Selection
    selected_products = models.ManyToManyField(
        "products.Product",  # Use string reference to avoid circular import
        through="EventProduct",
        related_name="events",
        verbose_name="Selected Products",
    )

    # Staff Assignment
    assigned_staff = models.ManyToManyField(Employee, related_name="assigned_events", blank=True)

    # Logistics
    decorations_required = models.BooleanField(default=False, verbose_name="Decorations Required")
    logistics_notes = models.TextField(blank=True, null=True, verbose_name="Logistics Notes")

    # Financial Information
    price_per_table = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name="Price per Table", default=0.00)
    number_of_tables = models.PositiveIntegerField(verbose_name="Number of Tables", blank=True, default=0)
    price_of_decoration = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name="Price of Decoration", default=0.00)
    price_of_extras = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name="Price of Extras", default=0.00)
    event_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Event Cost", default=0.00, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount Paid", default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Payment Status")

    # Status and Notes
    event_status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='scheduled', blank=True, verbose_name="Event Status")
    event_notes = models.TextField(blank=True, null=True, verbose_name="Event Notes")

    def calculate_total_price(self):
        """
        Calculate the total price of the event.
        Formula: (Price Per Table x Number of Tables) + Price of Decoration + Price of Extras
        """
        return (
            self.price_per_table * self.number_of_tables
            + self.price_of_decoration
            + self.price_of_extras
        )

    @property
    def total_price(self):
        """
        Return the dynamically calculated total price.
        """
        return self.calculate_total_price()

    def balance_due(self):
        """
        Return the balance due for the event.
        """
        return self.event_cost - self.amount_paid

    def calculate_product_quantities(self):
        """
        Calculate the quantities of selected products based on the number of tables.
        """
        event_products = self.eventproduct_set.all()
        for event_product in event_products:
            event_product.quantity = self.number_of_tables * 10
            event_product.save()

    def __str__(self):
        return f"{self.name} ({self.get_event_status_display()}) - {self.date}"

    def allocated_resources(self):
        """
        Return the resources allocated for this event.
        """
        return self.allocations.all()


class EventProduct(models.Model):
    """
    Intermediate model for associating products with events.
    Includes quantity and price information.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Event")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, verbose_name="Product")  # Use string reference
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")

    def __str__(self):
        return f"{self.product.name} for {self.event.name}"
