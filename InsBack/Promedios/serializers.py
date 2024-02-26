from rest_framework import serializers
from .models import *

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

    def create(self,validated_data):
        return Estudiante.objects.create(**validated_data)
    
class CursoSerializer(serializers.ModelSerializer):
    estudiantes = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = ('nombre', 'estudiantes')
    
    def get_estudiantes(self, obj):
        estudiantes = obj.estudiantes.all().distinct()
        return [estudiante.nombre for estudiante in estudiantes]

    def create(self,validated_data):
        return Curso.objects.create(**validated_data)

class NotaSerializer(serializers.ModelSerializer):
    estudiante = serializers.SerializerMethodField()
    curso = serializers.SerializerMethodField()

    class Meta:
        model = Nota
        fields = ('estudiante', 'curso' , 'nota')

    def get_estudiante(self, obj):
        return obj.estudiante.nombre
    
    def get_curso(self, obj):
        return obj.curso.nombre
    
    def create(self,validated_data):
        return Nota.objects.create(**validated_data)
    
class PromedioSerializer(serializers.ModelSerializer):
    estudiante = serializers.SerializerMethodField()
    curso = serializers.SerializerMethodField()

    class Meta:
        model = Promedio
        fields = ('promedio', 'estudiante', 'curso')

    def get_estudiante(self, obj):
        return obj.estudiante.nombre
    
    def get_curso(self, obj):
        return obj.curso.nombre

    def create(self,validated_data):
        return Nota.objects.create(**validated_data)