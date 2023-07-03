from django.db import models
from django.contrib.auth.models import User


class VirtualMachine(models.Model):
    name = models.CharField(max_length=100)
    appname = models.CharField(max_length=100)
    appversion = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
#End_class


class Resources(models.Model):
    os = models.CharField(max_length=50)
    vcpu = models.CharField(max_length=15)
    vram = models.CharField(max_length=15)
    vdisk = models.CharField(max_length=15)
    virtualmachines = models.ManyToManyField(VirtualMachine)

    def __str__(self):
        return self.os
#End_class


class Services(models.Model):
    choice = models.CharField(max_length=60)
    description = models.CharField(max_length=60)

    def __str__(self):
        return self.description
#End_class

