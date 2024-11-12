from django.urls import path
from .views import nuevoHello, bye, edad

urlpatterns = [
    path('hello', nuevoHello),
    path('bye', bye),
    path('edad/<int:anios>/<int:futuro>', edad)
]