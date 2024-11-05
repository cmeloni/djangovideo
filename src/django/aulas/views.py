#from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def nuevoHello(request):
    return HttpResponse("Hola mundo!!!")
