from django.contrib import admin
from .models import Dish, Menu

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'dish_type', 'price']
    list_filter = ['dish_type']
    search_fields = ['name']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'starter_dish', 'first_main_plate', 'second_main_plate', 'dessert']
    search_fields = ['name']
