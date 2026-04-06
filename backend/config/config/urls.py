# config/urls.py
from django.contrib import admin
from django.urls import path, include
from api.views import backend_status

urlpatterns = [
    path('', backend_status),              # /
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
