from django.urls import path
from .views import nuevoHello

urlpatterns = [
    path('hello', nuevoHello),
]