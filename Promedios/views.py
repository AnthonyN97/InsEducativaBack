from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets

from .models import *
from .serializers import *

class IndexView(APIView):
    def get(self,request):
        context = {'mensaje':'servidor activo'}
        return Response(context)

class EstudianteView(APIView):
    def get(self, request):
        dataEstudiante = Estudiante.objects.all()
        serEstudiante = EstudianteSerializer(dataEstudiante,many=True)
        return Response(serEstudiante.data)
    
    def post(self,request):
        serEstudiante = EstudianteSerializer(data=request.data)
        serEstudiante.is_valid(raise_exception=True)
        serEstudiante.save()
        return Response(serEstudiante.data)
    
class EstudianteDetailView(APIView):
    def get(self, request, id_estudiante):
        dataEstudiante = Estudiante.objects.filter(id=id_estudiante)
        serEstudiante = EstudianteSerializer(dataEstudiante,many=True)
        return Response(serEstudiante.data)
    
    def put(self,request,id_estudiante):
        dataEstudiante = Estudiante.objects.get(pk=id_estudiante)
        serEstudiante = EstudianteSerializer(dataEstudiante,data=request.data)
        serEstudiante.is_valid(raise_exception=True)
        serEstudiante.save()
        return Response(serEstudiante.data)
    
    def delete(self,request,id_estudiante):
        dataEstudiante = Estudiante.objects.get(pk=id_estudiante)
        serEstudiante = EstudianteSerializer(dataEstudiante)
        dataEstudiante.delete()
        return Response({"message": "Se elimno correctamente", "estudiante": serEstudiante.data})
    
class CursoView(APIView):
    def get(self, request):
        dataCurso = Curso.objects.all()
        serCurso = CursoSerializer(dataCurso,many=True)
        return Response(serCurso.data)
    
    def post(self,request):
        print(request.data)
        serCurso = CursoPostSerializer(data=request.data)
        serCurso.is_valid(raise_exception=True)
        serCurso.save()
        return Response(serCurso.data)
    
class CursoDetailView(APIView):
    def get(self, request, id_curso):
        dataCurso = Curso.objects.filter(id=id_curso)
        serCurso = CursoSerializer(dataCurso,many=True)
        return Response(serCurso.data)
    
    def put(self,request,id_curso):
        dataCurso = Curso.objects.get(pk=id_curso)
        serCurso = CursoPostSerializer(dataCurso,data=request.data)
        serCurso.is_valid(raise_exception=True)
        print(dataCurso, "-----", serCurso)
        serCurso.save()
        return Response(serCurso.data)
    
    def delete(self,request,id_curso):
        dataCurso = Curso.objects.get(pk=id_curso)
        serCurso = CursoSerializer(dataCurso)
        dataCurso.delete()
        return Response({"message": "Se elimno correctamente"})
    
class NotaView(APIView):
    def get(self, request):
        dataNota = Nota.objects.all()
        serNota = NotaSerializer(dataNota,many=True)
        return Response(serNota.data)
    
    def post(self,request):
        serNota = NotaPostSerializer(data=request.data)
        serNota.is_valid(raise_exception=True)
        serNota.save()
        return Response(serNota.data)

class NotaDetailView(APIView):
    def get(self, request, id_nota,id_estudiante):
        dataNota = Nota.objects.filter(id=id_nota)
        serNota = NotaSerializer(dataNota,many=True)
        return Response(serNota.data)
    
    def put(self,request,id_nota , id_estudiante):
        dataNota = Nota.objects.get(pk=id_nota)
        print(dataNota, request)
        serNota = NotaPostSerializer(dataNota,data=request.data)
        serNota.is_valid(raise_exception=True)
        eliminar_promedio_si_necesario(id_estudiante, dataNota.curso_id)
        serNota.save()
        return Response(serNota.data)
    
    def delete(self,request,id_nota, id_estudiante):
        dataNota = Nota.objects.get(pk=id_nota)
        serNota = NotaSerializer(dataNota)
        dataNota.delete()
        eliminar_promedio_si_necesario(id_estudiante, dataNota.curso_id)
        return Response({"message": "Se elimno correctamente", "nota": serNota.data})

    
class NotasAlumView(APIView):
    def get(self, request, id_estudiante):
        estudiante = Estudiante.objects.get(id=id_estudiante)
        dataNota = Nota.objects.filter(estudiante=estudiante)
        serNota = NotaSerializer(dataNota,many=True)
        return Response(serNota.data)
    
class PromedioView(APIView):
    def get(self, request):
        dataPromedio = Promedio.objects.all()
        serPromedio = PromedioSerializer(dataPromedio,many=True)
        return Response(serPromedio.data)
    

def eliminar_promedio_si_necesario(estudiante_id, curso_id):
    notas_restantes = Nota.objects.filter(estudiante_id=estudiante_id, curso_id=curso_id)
    if not notas_restantes.exists():
        # Si no hay más notas, eliminar también el objeto Promedio
        Promedio.objects.filter(estudiante_id=estudiante_id, curso_id=curso_id).delete()