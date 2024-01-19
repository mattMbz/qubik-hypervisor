'''app_hypervisor URL Configuration'''
from django.urls import path

from . import views
from app_setup.views import setup_virtual_machine

urlpatterns = [
    path("monitor/", views.monitor, name="monitor"),
    path("tasks/", views.tasks, name="tasks"),
    path("create-vm/", views.create_virtual_machine, name="create-vm"),
    path("delete-vm/", views.delete, name="delete-vm"),
    path("setup-vm/", setup_virtual_machine, name="setup-vm"),
    path("delete-vm/<str:vm_uuid>", views.delete, name='delete-vm-with-id'),
    path("start-vm/<str:vm_uuid>", views.start, name="start-vm-with-id"),
    path("shutdown-vm/<str:vm_uuid>", views.shutdown, name="shutdown-vm-with-id"),
    path("status-vm/<str:vm_uuid>", views.status, name="checking-vm-status"),
]
