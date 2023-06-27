from django.shortcuts import render
from django.http import HttpResponse

def monitor(request):
    return HttpResponse("MONITOR ...")

def tasks(request):
    return HttpResponse("TASKS ...")

def addvm(request):
    return HttpResponse("ADD NEW VIRTUAL MACHINE ...")

def delete(request):
    return HttpResponse("DELETE VIRTUAL MACHINE ...")