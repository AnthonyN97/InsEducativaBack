from datetime import date
from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
    
class Estudiante(models.Model):
    SEXO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    TIPO_SANGRE_OPCIONES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200)
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES, blank=True)
    fecha_nacimiento = models.DateField(default=date.today ,auto_now_add=False, auto_now=False, blank=True)
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_OPCIONES, blank=True)

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    estudiantes = models.ManyToManyField(Estudiante, through='Nota')
    
    def __str__(self):
        return self.nombre

class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nota = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(20.0)],)
    porcentaje = models.FloatField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        promedio, created = Promedio.objects.get_or_create(estudiante=self.estudiante, curso=self.curso)
        notas = Nota.objects.filter(estudiante=self.estudiante, curso=self.curso)
        promedio.promedio = sum(nota.nota * nota.porcentaje for nota in notas) / sum(nota.porcentaje for nota in notas)
        promedio.save()

    def __str__(self):
        return 'Estudiante: ' + self.estudiante.nombre + ' , curso: ' + self.curso.nombre

class Promedio(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    promedio = models.FloatField()

    def save(self, *args, **kwargs):
        notas = Nota.objects.filter(estudiante=self.estudiante, curso=self.curso)
        self.promedio = sum(nota.nota * nota.porcentaje for nota in notas) / sum(nota.porcentaje for nota in notas)
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Estudiante: ' + self.estudiante.nombre + ' , curso: ' + self.curso.nombre + ' , promedio: ' + str(self.promedio)