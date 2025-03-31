from django.contrib import admin
from aulas.models import Person, Musician, Album
# Register your models here.

admin.site.register(Person)
admin.site.register(Musician)
admin.site.register(Album)