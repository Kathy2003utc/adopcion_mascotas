from django.db import models

class Persona(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    correo = models.EmailField(unique=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, choices=[
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Otro', 'Otro'),
    ])
    raza = models.CharField(max_length=100, blank=True, null=True)
    edad = models.PositiveIntegerField(help_text="Edad en años aproximada")
    sexo = models.CharField(max_length=10, choices=[
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ])
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('Disponible', 'Disponible'),
        ('Adoptado', 'Adoptado'),
        ('En revisión', 'En revisión'),
    ], default='Disponible')
    fecha_ingreso = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to='mascotas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.especie})"


class Adopcion(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='adopciones')
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE, related_name='adopcion')
    fecha_adopcion = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.persona} adoptó a {self.mascota}"
