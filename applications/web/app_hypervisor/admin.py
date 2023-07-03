from django.contrib import admin

# Register your models here.
from .models import VirtualMachine, Resources

admin.site.register(VirtualMachine)
admin.site.register(Resources)
