from datetime import date
from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
    
class Estudiante(models.Model):
    SEXO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    GRADO_OPCIONES = [
        ('1ro de primaria', 'Primero de Primaria'),
        ('2do de primaria', 'Segundo de Primaria'),
        ('3ro de primaria', 'Tercero de Primaria'),
        ('4to de primaria', 'Cuarto de Primaria'),
        ('5to de primaria', 'Quinto de Primaria'),
        ('6to de primaria', 'Sexto de Primaria'),
        ('1ro de secundaria', 'Primero de Secundaria'),
        ('2do de secundaria', 'Segundo de Secundaria'),
        ('3ro de secundaria', 'Tercero de Secundaria'),
        ('4to de secundaria', 'Cuarto de Secundaria'),
        ('5to de secundaria', 'Quinto de Secundaria'),
    ]

    SECCION_OPCIONES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
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
    grado = models.CharField(max_length=20, choices=GRADO_OPCIONES, blank=True)
    seccion = models.CharField(max_length=1, choices=SECCION_OPCIONES, blank=True)
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_OPCIONES, blank=True)

    def __str__(self):
        return self.nombre + ' ' + str(self.id)

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    users = models.ManyToManyField(User, blank=True)
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