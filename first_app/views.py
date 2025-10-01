from django.shortcuts import render, HttpResponse 

def hello(request):
    text = 'Lorem ipsum'
    return render(request, 'one.html', {'my_note': text})