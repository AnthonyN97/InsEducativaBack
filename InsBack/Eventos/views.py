from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Eventos
from .serializers import EventoSerializer

class IndexView(APIView):
    def get(self,request):
        context = {'mensaje':'servidor activo'}
        return Response(context)
    
class EventosView(APIView):
    
    def get(self,request):
        dataEventos = Eventos.objects.all()
        serEventos = EventoSerializer(dataEventos,many=True)
        return Response(serEventos.data)
    
    """def post(self,request):
        serEventos = EventoSerializer(data=request.data)
        serEventos.is_valid(raise_exception=True)
        serEventos.save()
        
        return Response(serEventos.data)"""
    
class EventoDetailView(APIView):
    def get(self,request,Evento_id):
        dataEvento = Eventos.objects.get(pk=Evento_id)
        serEvento = EventoSerializer(dataEvento)
        return Response(serEvento.data)
    
    """def put(self,request,Evento_id):
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
