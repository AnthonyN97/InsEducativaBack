from rest_framework import serializers
from django.shortcuts import get_object_or_404
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
        fields = ('id','nombre', 'estudiantes' )
    
    def get_estudiantes(self, obj):
        estudiantes = obj.estudiantes.all().distinct()
        return [{'id': estudiante.id, 'nombre': estudiante.nombre} for estudiante in estudiantes]


class CursoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ('nombre', 'estudiantes')

    def create(self, validated_data):
        nombre = validated_data.pop('nombre')
        return Curso.objects.create(nombre=nombre , **validated_data)

class NotaSerializer(serializers.ModelSerializer):
    estudiante_id = serializers.SerializerMethodField()
    estudiante = serializers.SerializerMethodField()
    curso_id = serializers.SerializerMethodField()
    curso = serializers.SerializerMethodField()

    class Meta:
        model = Nota
        fields = ('id','estudiante_id', 'estudiante', 'curso_id','curso' , 'nota', 'porcentaje')

    def get_estudiante_id(self, obj):
        return obj.estudiante.id

    def get_estudiante(self, obj):
        return obj.estudiante.nombre
    
    def get_curso_id(self, obj):
        return obj.curso.id
    
    def get_curso(self, obj):
        return obj.curso.nombre
    
class NotaPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ('estudiante', 'curso', 'nota', 'porcentaje')

    def create(self, validated_data):
        estudiante = validated_data.pop('estudiante')
        curso = validated_data.pop('curso')
        
        return Nota.objects.create(
            estudiante=estudiante,
            curso=curso,
            nota=validated_data.get('nota'),
            porcentaje=validated_data.get('porcentaje')
        )
        
class NotaCreateSerializer(serializers.Serializer):
    estudiante = serializers.CharField()
    curso = serializers.CharField()
    nota = serializers.FloatField()
    porcentaje = serializers.FloatField()

    def create(self, validated_data):
        # Obtener el nombre del curso
        curso_nombre = validated_data.pop('curso')  # Remover el campo curso para buscar el objeto
        estudiante_nombre = validated_data.pop('estudiante')
        # Obtener el objeto Curso usando el nombre
        curso = get_object_or_404(Curso, nombre=curso_nombre)
        estudiante = get_object_or_404(Estudiante, nombre=estudiante_nombre)
        # Crear la nota usando el objeto Curso
        nota = Nota.objects.create(estudiante=estudiante,curso=curso, **validated_data)  # Suponiendo que Nota tiene un campo 'curso'
        return nota

class MultipleNotaPostSerializer(serializers.Serializer):
    notas = NotaCreateSerializer(many=True)

    def create(self, validated_data):
        notas_data = validated_data['notas']
        notas = []

        for nota_data in notas_data:
            # Crear una nota usando el serializer de creación
            nota = NotaCreateSerializer().create(nota_data)
            notas.append(nota)

        return notas  # Retornar las notas creadas
    
class PromedioSerializer(serializers.ModelSerializer):
    estudiante = serializers.SerializerMethodField()
    curso = serializers.SerializerMethodField()
    grado = serializers.SerializerMethodField()
    seccion = serializers.SerializerMethodField()

    class Meta:
        model = Promedio
        fields = ( 'estudiante','grado', 'seccion','curso', 'promedio')

    def get_estudiante(self, obj):
        return obj.estudiante.nombre
    
    def get_curso(self, obj):
        return obj.curso.nombre
    
    def get_seccion(self, obj):
        return obj.estudiante.seccion
    
    def get_grado(self, obj):
        return obj.estudiante.grado

    def create(self,validated_data):
        return Nota.objects.create(**validated_data)
    
class PromedioEstSerializer(serializers.ModelSerializer):
    promedios = serializers.SerializerMethodField()
    grado = serializers.SerializerMethodField()
    seccion = serializers.SerializerMethodField()

    class Meta:
        model = Estudiante
        fields = ('id', 'nombre', 'grado','seccion','promedios')
        
    def get_seccion(self, obj):
        return obj.seccion
    
    def get_grado(self, obj):
        return obj.grado

    def get_promedios(self, obj):
        nombre_estudiante = obj.nombre
        promedios = Promedio.objects.filter(estudiante__nombre=nombre_estudiante)
        promedios_list = [{'curso': promedio.curso.nombre, 'promedio': promedio.promedio} for promedio in promedios]

        return promedios_list