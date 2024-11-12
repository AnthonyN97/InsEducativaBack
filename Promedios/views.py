from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import status
import psutil
import os

class EstudianteView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cursos_usuario = Curso.objects.filter(users=request.user)
        dataNota = Nota.objects.filter(curso__in=cursos_usuario)
        serNota = NotaSerializer(dataNota,many=True)
        return Response(serNota.data)
    
    def post(self, request):
        print(request.data)

        if isinstance(request.data, list):
            print("paso2")
            serializer = MultipleNotaPostSerializer(data={"notas":request.data})  # Crea el serializador

            # Validar y guardar
            if serializer.is_valid(raise_exception=True):  # Esto lanzará un error si la validación falla
                notas = serializer.save()  # Aquí se llama a create
                # Serializar la lista de notas para la respuesta
                serNota = NotaSerializer(notas, many=True)  # Serializar las notas
                return Response(serNota.data, status=status.HTTP_201_CREATED)
            else:
                print("Errores de validación:", serializer.errors)  # Imprimir errores de validación
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Si es una sola nota
            serializer = NotaPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            notas = serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NotaDetailView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    def get(self, request, id_estudiante):
        estudiante = Estudiante.objects.get(id=id_estudiante)
        dataNota = Nota.objects.filter(estudiante=estudiante)
        serNota = NotaSerializer(dataNota,many=True)
        return Response(serNota.data)
    
class PromedioView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        dataPromedio = Promedio.objects.all()
        serPromedio = PromedioSerializer(dataPromedio,many=True)
        return Response(serPromedio.data)
    
class PromedioPorEstudianteView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        dataPromedioEst = Estudiante.objects.all()
        serPromedioEst = PromedioEstSerializer(dataPromedioEst,many=True)
        return Response(serPromedioEst.data)
    
def log_memory_usage():
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024 / 1024  # Convertir a GB
    print(f"Uso de memoria: {memory_usage:.4f} GB")

class NotaPromPorPadreView(APIView):
    def post(self, request):
        id_estudiante = request.data.get('id_estudiante')
        if not id_estudiante:
            return Response({'error': 'ID del estudiante es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uuid.UUID(id_estudiante)
        except ValueError:
            return Response({'error': 'ID del estudiante no es un UUID válido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            estudiante = Estudiante.objects.get(id=id_estudiante)
            # Optimización: usar select_related y values para obtener solo los datos necesarios
            notas = Nota.objects.filter(estudiante=estudiante).select_related('curso').values('curso__nombre', 'nota', 'porcentaje')
            promedios = Promedio.objects.filter(estudiante=estudiante).select_related('curso').values('curso__nombre', 'promedio')

            # Construcción directa de datos, sin listas intermedias
            data = {
                'estudiante': estudiante.nombre,
                'notas': list(notas),
                'promedios': list(promedios)
            }

            log_memory_usage()  # Registrar el uso de memoria después de generar el objeto de respuesta
            return Response(data, status=status.HTTP_200_OK)
        
        except Estudiante.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)

def eliminar_promedio_si_necesario(estudiante_id, curso_id):
    notas_restantes = Nota.objects.filter(estudiante_id=estudiante_id, curso_id=curso_id)
    if not notas_restantes.exists():
        # Si no hay más notas, eliminar también el objeto Promedio
        Promedio.objects.filter(estudiante_id=estudiante_id, curso_id=curso_id).delete()