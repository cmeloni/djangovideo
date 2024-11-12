#from django.shortcuts import render
from django.http import HttpResponse
from datetime import date


# Create your views here.
def nuevoHello(request):
    return HttpResponse("Hola mundo!!!")


def bye(request):
    return HttpResponse("Hasta luego!!!")

def edad(request, anios, futuro):
    incremento = futuro - date.today().year
    cumplira = anios + incremento
    mensaje = "En el año %d cumpliras %d años"%( futuro, cumplira)

    return HttpResponse(mensaje)
