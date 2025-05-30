from rest_framework import serializers


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