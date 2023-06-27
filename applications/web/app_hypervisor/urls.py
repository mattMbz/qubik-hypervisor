'''app_hypervisor URL Configuration'''
from django.urls import path

from . import views

urlpatterns = [
    path("monitor/", views.monitor, name="monitor"),
    path("tasks/", views.tasks, name="tasks"),
    path("add-vm/", views.addvm, name="add-vm"),
    path("delete-vm/", views.delete, name="delete-vm")
]
