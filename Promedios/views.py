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
    
"""class EventosView(APIView):
    
    def get(self,request):
        dataEventos = Eventos.objects.all()
        serEventos = EventoSerializer(dataEventos,many=True)
        return Response(serEventos.data)
    
    def post(self,request):
        serEventos = EventoSerializer(data=request.data)
        serEventos.is_valid(raise_exception=True)
        serEventos.save()
        
        return Response(serEventos.data)
    
class EventoDetailView(APIView):
    def get(self,request,Evento_id):
        dataEvento = Eventos.objects.get(pk=Evento_id)
        serEvento = EventoSerializer(dataEvento)
        return Response(serEvento.data)
    
    Edef put(self,request,Evento_id):
        dataEvento = Eventos.objects.get(pk=Evento_id)
        serEvento = EventoSerializer(dataEvento,data=request.data)
        serEvento.is_valid(raise_exception=True)
        serEvento.save()
        return Response(serEvento.data)
    
    def delete(self,request,Evento_id):
        dataEvento = Eventos.objects.get(pk=Evento_id)
        serEvento = EventoSerializer(dataEvento)
        dataEvento.delete()
        return Response(serEvento.data)"""

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
    
class CursoView(APIView):
    def get(self, request):
        dataCurso = Curso.objects.all()
        serCurso = CursoSerializer(dataCurso,many=True)
        return Response(serCurso.data)
    
class NotaView(APIView):
    def get(self, request):
        dataNota = Nota.objects.all()
        serNota = NotaSerializer(dataNota,many=True)
        return Response(serNota.data)
    
class NotasAlumView(APIView):
    def get(self, request, id):
        estudiante = Estudiante.objects.get(id=id)
        dataNota = Nota.objects.filter(estudiante=estudiante)
        serNota = NotaSerializer(dataNota,many=True)
        return Response(serNota.data)
    
class PromedioView(APIView):
    def get(self, request):
        dataPromedio = Promedio.objects.all()
        serPromedio = PromedioSerializer(dataPromedio,many=True)
        return Response(serPromedio.data)