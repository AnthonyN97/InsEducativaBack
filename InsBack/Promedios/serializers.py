from rest_framework import serializers
from .models import *

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

    def create(self,validated_data):
        return Estudiante.objects.create(**validated_data)
    
class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ('nombre', 'estudiantes')

    def create(self,validated_data):
        return Curso.objects.create(**validated_data)

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ('estudiante', 'curso' , 'nota')

    def create(self,validated_data):
        return Nota.objects.create(**validated_data)
    
