'''app_hypervisor URL Configuration'''
from django.urls import path

from . import views

urlpatterns = [
    path("monitor/", views.monitor, name="monitor"),
    path("tasks/", views.tasks, name="tasks"),
    path("create-vm/", views.create_virtual_machine, name="create-vm"),
    path("delete-vm/", views.delete, name="delete-vm")
]
