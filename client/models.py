from django.db import models

class Customer(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    address = models.TextField(verbose_name="Address")

    def __str__(self):
        return self.full_name
