from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'total_quantity', 'quantity_available')
    search_fields = ('name', 'category')

# @admin.register(MaterialAllocation)
# class MaterialAllocationAdmin(admin.ModelAdmin):
#     list_display = ('material', 'event', 'quantity_allocated', 'date_allocated')
#     list_filter = ('event',)
