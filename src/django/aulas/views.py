#from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from .models import Musician, Album

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

def primer_plantilla(request):
    plantilla = """
    <html>
      <body>
        <h2>
            Hola {{ nombre }}! esta es mi primer plantilla!
        </h2>
      </body>
    </html>
    """

    tpl = Template(plantilla)
    ctx = Context({
        'nombre': 'Juan Perez'
    })
    mensaje = tpl.render(ctx)

    return HttpResponse(mensaje)

def segunda_plantilla(request):

    tpl = get_template("segunda_plantilla.html")
    mensaje = tpl.render({
        'nombre': 'Juan Gonzalez',
        'fecha_actual': date.today()
    })
    return HttpResponse(mensaje)

def tercer_plantilla(request):

    return render(request, "tercer_plantilla.html", {
        'nombre': 'Pedro Gomez',
        'fecha_actual': date.today()
    })

class Empleado(object):

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

def cuarta_plantilla(request):

    empleado = Empleado("Juan", "Gomez")

    laborables = ['Lunes', 'Martes', 'Miécoles', 'Jueves']

    return render(request, "cuarta_plantilla.html", {
        'mi_empleado': empleado,
        'fecha_actual': date.today(),
        'dias_laborables': laborables
    })



def crear_musico(request, nombre, apellido, instrumento):
    per=Musician(first_name=nombre, last_name=apellido, instrument=instrumento)
    per.save()
    mensaje = "Se creó el músico %s %s con id %d"%( per.first_name, per.last_name, per.id)

    return HttpResponse(mensaje)

def crear_albun(request, nombre, estrellas, artista_id):
    art=Musician.objects.get(id=artista_id)
    albun=Album(name=nombre, release_date=date.today(), num_stars=estrellas, artist=art)
    albun.save()
    mensaje = "Se creó el Albun %s del Artista %s con id %d"%( albun.name, art.last_name, albun.id)

    return HttpResponse(mensaje)
