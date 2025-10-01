from django.shortcuts import render, HttpResponse 
from .models import Users

def root(request):
    test = request.GET['test'] 
    # if request.method == 'POST':
    #     a = Users()
    #     Users.save()
    # elif request.method == 'GET':
    #     return render ('', {'users':Users.objects.all()})
    
    # return render(request, 'one.html', {'my_note': text})