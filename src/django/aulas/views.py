#from django.shortcuts import render
import json

from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics


from .models import Musician, Album, Person
from .serializers import PersonaSerializer, PersonSerializer


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

@permission_classes('rest_framework.permissions.IsAdminUser')
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

@csrf_exempt
def first_api(request):
    if request.method == 'GET':
        respuesta = {
            'nombre': 'Juan',
            'apellido': 'Perez',
            'edad': 25
        }
        return JsonResponse(respuesta)
    elif request.method == 'POST':
        datos = json.loads(request.body)
        nombre = datos['nombre']
        apellido = datos['apellido']
        edad = datos['edad']
        respuesta = {
            'nombre2': nombre,
            'apellido2': apellido,
            'edad2': edad
        }
        return JsonResponse(respuesta)
    return None

@csrf_exempt
def serial_v1(request):
    if request.method == 'POST':
        datos = json.loads(request.body)
        serializador = PersonaSerializer(data=datos)
        if serializador.is_valid():
            return JsonResponse(serializador.validated_data, status=201)
        else:
            return JsonResponse(serializador.errors, status=400)
    return None

@csrf_exempt
def person_list(request):

    if request.method == 'GET':
        personas = Person.objects.all()
        serializer = PersonSerializer(personas, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        datos = json.loads(request.body)
        serializer = PersonSerializer(data=datos)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    return None

@csrf_exempt
def person_detail(request, pk):

    if request.method == 'GET':
        persona = Person.objects.get(pk=pk)
        serializer = PersonSerializer(persona)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'PUT':
        datos = json.loads(request.body)
        persona = Person.objects.get(pk=pk)
        serializer = PersonSerializer(persona, data=datos)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        persona = Person.objects.get(pk=pk)
        persona.delete()
        return HttpResponse(status=204)

    return None


class PersonAPIView(APIView):
    """
    List all Persons, or create a new Person.
    """
    def get(self, request, format=None):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonAPIDetail(APIView):
    """
    Retrieve, update or delete a Person instance.
    """
    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        person = self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonMixinList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PersonMixinDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

##DRY!!!! please!

class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
