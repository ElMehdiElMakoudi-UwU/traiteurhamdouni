from django.db import models
from client.models import Customer
from menu.models import Menu
from employees.models import Employee


class Event(models.Model):
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('corporate', 'Corporate Event'),
        ('birthday', 'Birthday'),
        ('private', 'Private Party'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ]

    EVENT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Basic Information
    name = models.CharField(max_length=255, verbose_name="Event Name")
    date = models.DateField(verbose_name="Event Date")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES,blank=True, verbose_name="Event Type")

    # Client Information
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="events")
    number_of_guests = models.PositiveIntegerField(blank=True, verbose_name="Number of Guests")

    # Venue Information
    venue_name = models.CharField(max_length=255,blank=True, verbose_name="Venue Name")
    venue_address = models.TextField(blank=True, verbose_name="Venue Address")
    venue_contact = models.CharField(max_length=20, verbose_name="Venue Contact", blank=True, null=True)

    # Menu Information
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Menu")
    special_instructions = models.TextField(blank=True, null=True, verbose_name="Special Instructions")

    # Staff Assignment
    assigned_staff = models.ManyToManyField(Employee, related_name="assigned_events", blank=True)

    # Logistics
    decorations_required = models.BooleanField(default=False, verbose_name="Decorations Required")
    logistics_notes = models.TextField(blank=True, null=True, verbose_name="Logistics Notes")

    # Financial Information
    price_per_table = models.DecimalField(max_digits=10, decimal_places=2,blank=True, verbose_name="Price per Table", default=0.00)
    number_of_tables = models.PositiveIntegerField(verbose_name="Number of Tables",blank=True, default=0)
    price_of_decoration = models.DecimalField(max_digits=10, decimal_places=2,blank=True, verbose_name="Price of Decoration", default=0.00)
    price_of_extras = models.DecimalField(max_digits=10, decimal_places=2,blank=True, verbose_name="Price of Extras", default=0.00)
    event_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Event Cost", default=0.00, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount Paid", default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Payment Status")

    # Status and Notes
    event_status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='scheduled',blank=True, verbose_name="Event Status")
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

    def __str__(self):
        return f"{self.name} ({self.get_event_status_display()}) - {self.date}"
    
    def allocated_resources(self):
        """
        Return the resources allocated for this event.
        """
        return self.allocations.all()
