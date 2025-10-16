from django.shortcuts import render, HttpResponse 
from .models import Users

def root(request):
    return render(request, 'main.catalog.html')