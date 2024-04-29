from django.urls import path

from .consumers import WSConsumer, VMResourcesConsumer

ws_urlpatterns = [
    path('ws/hypervisor_monitor/', WSConsumer.as_asgi()),
    path('ws/virtualmachine_monitor/', VMResourcesConsumer.as_asgi())
]