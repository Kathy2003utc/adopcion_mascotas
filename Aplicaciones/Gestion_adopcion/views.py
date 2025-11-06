from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Persona, Mascota
from django.db import IntegrityError

# Listar personas
def listaPersonas(request):
    personaListado = Persona.objects.all()
    return render(request, "personas/lista.html", {'Personas': personaListado})

# Mostrar formulario para nueva persona
def nuevaPersona(request):
    return render(request, "personas/crear.html")

# Guardar nueva persona
def guardarPersona(request):
    if request.method == "POST":
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        cedula = request.POST['cedula']
        telefono = request.POST.get('telefono', '')
        direccion = request.POST.get('direccion', '')
        correo = request.POST['correo']

        try:
            Persona.objects.create(
                nombres=nombres,
                apellidos=apellidos,
                cedula=cedula,
                telefono=telefono,
                direccion=direccion,
                correo=correo
            )
            messages.success(request, "Persona registrada exitosamente")
            return redirect('lista_personas')
        except IntegrityError:
            # Mensaje si la cédula ya existe
            messages.error(request, f"La cédula {cedula} ya está registrada.")
            return redirect('crear_persona')
    else:
        return redirect('crear_persona')
# Eliminar persona
def eliminarPersona(request, id):
    personaEliminar = Persona.objects.get(id=id)
    personaEliminar.delete()
    messages.success(request, "Persona eliminada exitosamente")
    return redirect('lista_personas')

# Mostrar formulario para editar persona
def editarPersona(request, id):
    personaEditar = Persona.objects.get(id=id)
    return render(request, "personas/editar.html", {
        'personaEditar': personaEditar
    })


# Procesar edición de persona
def procesarEdicionPersona(request):
    if request.method == "POST":
        id = request.POST['id']
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        cedula = request.POST['cedula']
        telefono = request.POST.get('telefono', '')
        direccion = request.POST.get('direccion', '')
        correo = request.POST['correo']

        persona = Persona.objects.get(id=id)

        # Verificar si la cédula ya existe en otra persona
        if Persona.objects.exclude(id=id).filter(cedula=cedula).exists():
            messages.error(request, f"La cédula {cedula} ya está registrada en otra persona.")
            return redirect('editar_persona', id=id)

        try:
            persona.nombres = nombres
            persona.apellidos = apellidos
            persona.cedula = cedula
            persona.telefono = telefono
            persona.direccion = direccion
            persona.correo = correo
            persona.save()
            messages.success(request, "Persona actualizada exitosamente")
            return redirect('lista_personas')
        except IntegrityError:
            messages.error(request, f"No se pudo actualizar los datos porque esa cedula ya existe.")
            return redirect('editar_persona', id=id)
    else:
        return redirect('lista_personas')


# Listar mascotas
def listaMascotas(request):
    mascotasListado = Mascota.objects.all()
    return render(request, "mascotas/lista.html", {'Mascotas': mascotasListado})

# Mostrar formulario para nueva mascota
def nuevaMascota(request):
    return render(request, "mascotas/crear.html")

# Guardar nueva mascota
def guardarMascota(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        especie = request.POST['especie']
        raza = request.POST.get('raza', '')
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        descripcion = request.POST.get('descripcion', '')
        estado = request.POST.get('estado', 'Disponible')
        foto = request.FILES.get('foto', None)

        Mascota.objects.create(
            nombre=nombre,
            especie=especie,
            raza=raza,
            edad=edad,
            sexo=sexo,
            descripcion=descripcion,
            estado=estado,
            foto=foto
        )
        messages.success(request, "Mascota registrada exitosamente")
        return redirect('lista_mascotas')
    else:
        return redirect('crear_mascota')

# Eliminar mascota
def eliminarMascota(request, id):
    mascotaEliminar = Mascota.objects.get(id=id)
    mascotaEliminar.delete()
    messages.success(request, "Mascota eliminada exitosamente")
    return redirect('lista_mascotas')

# Mostrar formulario para editar mascota
def editarMascota(request, id):
    mascotaEditar = Mascota.objects.get(id=id)
    return render(request, "mascotas/editar.html", {
        'mascotaEditar': mascotaEditar
    })

# Procesar edición de mascota
def procesarEdicionMascota(request):
    if request.method == "POST":
        id = request.POST['id']
        nombre = request.POST['nombre']
        especie = request.POST['especie']
        raza = request.POST.get('raza', '')
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        descripcion = request.POST.get('descripcion', '')
        estado = request.POST.get('estado', 'Disponible')
        foto = request.FILES.get('foto', None)

        mascota = Mascota.objects.get(id=id)
        mascota.nombre = nombre
        mascota.especie = especie
        mascota.raza = raza
        mascota.edad = edad
        mascota.sexo = sexo
        mascota.descripcion = descripcion
        mascota.estado = estado
        if foto:
            mascota.foto = foto
        mascota.save()

        messages.success(request, "Mascota actualizada exitosamente")
        return redirect('lista_mascotas')
    else:
        return redirect('lista_mascotas')