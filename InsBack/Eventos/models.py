from django.db import models

# Create your models here.
class Eventos(models.Model):

    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    lugar = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()