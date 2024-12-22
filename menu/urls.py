from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Dish URLs
    path('dishes/', views.dish_list, name='dish_list'),
    path('dishes/create/', views.create_dish, name='create_dish'),
    path('dishes/edit/<int:pk>/', views.edit_dish, name='edit_dish'),
    path('dishes/delete/<int:pk>/', views.delete_dish, name='delete_dish'),

    # Menu URLs
    path('menus/', views.menu_list, name='menu_list'),
    path('menus/create/', views.create_menu, name='create_menu'),
    path('menus/edit/<int:pk>/', views.edit_menu, name='edit_menu'),
    path('menus/delete/<int:pk>/', views.delete_menu, name='delete_menu'),
]
