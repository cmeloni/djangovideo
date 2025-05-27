from django.urls import path
from .views import nuevoHello, bye, edad, primer_plantilla, segunda_plantilla, tercer_plantilla, cuarta_plantilla, crear_musico, crear_albun, first_api

urlpatterns = [
    path('hello', nuevoHello),
    path('bye', bye),
    path('edad/<int:anios>/<int:futuro>', edad),
    path('plantilla1', primer_plantilla),
    path('plantilla2', segunda_plantilla),
    path('plantilla3', tercer_plantilla),
    path('plantilla4', cuarta_plantilla),
    path('crearmusico/<nombre>/<apellido>/<instrumento>', crear_musico),
    path('crearalbun/<nombre>/<int:estrellas>/<int:artista_id>', crear_albun),
    path('api/first_api', first_api),
]