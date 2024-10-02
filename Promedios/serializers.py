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
        fields = ('estudiante', 'curso' , 'nota', 'porcentaje')

    def create(self, validated_data):
        estudiante_id = validated_data.pop('estudiante')
        curso_id = validated_data.pop('curso')
        nota = validated_data.pop('nota')
        porcentaje = validated_data.pop('porcentaje')
        return Nota.objects.create(estudiante=estudiante_id, curso=curso_id, nota=nota, porcentaje=porcentaje, **validated_data)
    
class PromedioSerializer(serializers.ModelSerializer):
    estudiante = serializers.SerializerMethodField()
    curso = serializers.SerializerMethodField()
    grado = serializers.SerializerMethodField()
    seccion = serializers.SerializerMethodField()

    class Meta:
        model = Promedio
        fields = ( 'estudiante','grado', 'seccion','curso', 'promedio',)

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