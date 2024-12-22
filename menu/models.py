from django.db import models

class Dish(models.Model):
    DISH_TYPES = [
        ('starter', 'Starter Dish'),
        ('first_main', 'First Main Plate'),
        ('second_main', 'Second Main Plate'),
        ('dessert', 'Dessert'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Dish Name")
    dish_type = models.CharField(max_length=20, choices=DISH_TYPES, verbose_name="Dish Type")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")

    def __str__(self):
        return f"{self.name} ({self.get_dish_type_display()})"


class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name="Menu Name")
    starter_dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=False, related_name="starter_dishes")
    first_main_plate = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=False, related_name="first_main_dishes")
    second_main_plate = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=False, related_name="second_main_dishes")
    dessert = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=False, related_name="desserts")

    def __str__(self):
        return self.name
