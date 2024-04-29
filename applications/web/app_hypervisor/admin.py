from django.contrib import admin

# Register your models here.
from .models import VirtualMachine, Resources, Services

admin.site.register(VirtualMachine)
admin.site.register(Resources)
admin.site.register(Services)