from rest_framework import serializers
from .models import Person, Album, Musician

class PersonaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    edad = serializers.IntegerField()

    def validate_edad(self, value):
        if value < 18:
            raise serializers.ValidationError("Edad insuficiente")
        return value

    def validate_nombre(self, value):
        correcciones = {
            'hariel': 'Ariel',
            'jhon': 'John',
            'mariah': 'Maria'
        }
        valor_normalizado = value.strip().lower()
        return correcciones.get(valor_normalizado, value.strip().capitalize())


    def validate_apellido(self, value):
        return value.strip().capitalize()


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        #fields = ('id', 'first_name', 'last_name')

class AlbumSerializer(serializers.ModelSerializer):
    artist_firstname = serializers.ReadOnlyField(source='artist.first_name')
    artist_lastname = serializers.ReadOnlyField(source='artist.last_name')
    class Meta:
        model = Album
        fields = ('id', 'artist', 'name', 'release_date', 'num_stars', 'artist_firstname', 'artist_lastname')

class SimpleAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'name')


class MusicianSerializer(serializers.ModelSerializer):
    albums = SimpleAlbumSerializer(many=True, read_only=True)
    class Meta:
        model = Musician
        fields = ('id', 'first_name', 'last_name', 'instrument', 'albums')
