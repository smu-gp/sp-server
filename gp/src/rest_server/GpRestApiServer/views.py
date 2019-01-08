from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def GetImage(request):
    return HttpResponse("<h1>data transfer success<h1>")
