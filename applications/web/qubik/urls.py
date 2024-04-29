'''qubik URL Configuration'''

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app_main_panel.urls")),
    path('auth/', include("app_auth.urls")),
    path('hypervisor/', include("app_hypervisor.urls")),
]
