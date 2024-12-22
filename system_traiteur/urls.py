from django.contrib import admin
from django.urls import path, include
from client.views import home  # Import the home view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page
    path('client/', include('client.urls')),  # Replace 'your_app_name' with the name of your app
    path('menu/', include('menu.urls')),
    path('employees/', include('employees.urls')),
    path('events/', include('events.urls')),
    path('assignments/', include('assignments.urls')),
    path('materials/', include('materials.urls')),
    path('accounts/', include('accounts.urls')),
]
