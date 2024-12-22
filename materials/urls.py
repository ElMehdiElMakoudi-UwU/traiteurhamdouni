from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.material_list, name='list'),
    path('add/', views.add_material, name='add'),
    path('<int:pk>/edit/', views.edit_material, name='edit'),
    path('<int:pk>/delete/', views.delete_material, name='delete'),
]
