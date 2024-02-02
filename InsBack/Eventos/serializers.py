from rest_framework import serializers
from .models import Eventos

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ('id', 'titulo', 'descripcion', 'lugar', 'fecha_inicio', 'fecha_fin')

    def create(self,validated_data):
        return Eventos.objects.create(**validated_data)
