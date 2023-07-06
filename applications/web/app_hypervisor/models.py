from django.db import models
from django.contrib.auth.models import User


class Resources(models.Model):
    os = models.CharField(max_length=60)
    vcpu = models.CharField(max_length=30)
    vdisk = models.CharField(max_length=30)
    vram = models.CharField(max_length=30)

    def __str__(self):
        return self.os
#End_class


class Services(models.Model):
    choice = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
#End_class


class VirtualMachine(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100, null=True)
    app_version = models.CharField(max_length=10, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resources = models.OneToOneField(Resources, on_delete=models.CASCADE, default=None)
    creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['resources']),
            models.Index(fields=['user']),
        ]
    #End_class_Meta

    def __str__(self):
        return self.name
#End_class