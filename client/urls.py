from django.urls import path
from .views import add_customer, customer_list, edit_customer, delete_customer, customer_detail

urlpatterns = [
    path('add-customer/', add_customer, name='add_customer'),
    path('customer-list/', customer_list, name='customer_list'),
    path('edit-customer/<int:pk>/', edit_customer, name='edit_customer'),
    path('delete-customer/<int:pk>/', delete_customer, name='delete_customer'),
    path('customer-detail/<int:pk>/', customer_detail, name='customer_detail'),
]
