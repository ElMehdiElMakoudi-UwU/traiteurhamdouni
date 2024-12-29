from django.urls import path
from .views import product_form, product_list, product_order, delete_product
app_name = 'products'

urlpatterns = [
    path('', product_list, name='product_list'),  # List all products
    path('form/', product_form, name='add_product'),  # Add a new product
    path('form/<int:product_id>/', product_form, name='edit_product'),  # Edit an existing product
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path("order/<int:event_id>/", product_order, name="product_order"),
]
