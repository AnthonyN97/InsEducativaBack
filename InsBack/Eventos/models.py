from django.db import models

# Create your models here.
class Eventos(models.Model):

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)
    lugar = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.titulo
    
class Estudiante(models.Model):
    nombre = models.CharField(max_length=200)

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    estudiantes = models.ManyToManyField(Estudiante, through='Nota')

class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nota = models.FloatField()