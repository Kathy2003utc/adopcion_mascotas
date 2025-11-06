from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Persona, Mascota, Adopcion
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
    
    # Verificar si la persona tiene adopciones
    if Adopcion.objects.filter(persona=personaEliminar).exists():
        messages.error(request, "No se puede eliminar esta persona porque tiene adopciones registradas.")
    else:
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
    
    # Verificar si la mascota tiene adopciones
    if Adopcion.objects.filter(mascota=mascotaEliminar).exists():
        messages.error(request, "No se puede eliminar esta mascota porque está asociada a una adopción.")
    else:
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
    
# Guardar nueva mascota
def guardarMascota(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        especie = request.POST['especie']
        raza = request.POST.get('raza', '')
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        descripcion = request.POST.get('descripcion', '')
        foto = request.FILES.get('foto', None)

        # Siempre disponible al crear
        Mascota.objects.create(
            nombre=nombre,
            especie=especie,
            raza=raza,
            edad=edad,
            sexo=sexo,
            descripcion=descripcion,
            estado='Disponible',
            foto=foto
        )
        messages.success(request, "Mascota registrada exitosamente")
        return redirect('lista_mascotas')
    else:
        return redirect('crear_mascota')


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
        foto = request.FILES.get('foto', None)

        mascota = Mascota.objects.get(id=id)
        mascota.nombre = nombre
        mascota.especie = especie
        mascota.raza = raza
        mascota.edad = edad
        mascota.sexo = sexo
        mascota.descripcion = descripcion

        # No permitir cambiar el estado manualmente, se gestiona automáticamente
        if foto:
            mascota.foto = foto

        # Actualizar estado automáticamente según si tiene adopción
        if hasattr(mascota, 'adopcion'):
            mascota.estado = 'Adoptado'
        else:
            mascota.estado = 'Disponible'

        mascota.save()
        messages.success(request, "Mascota actualizada exitosamente")
        return redirect('lista_mascotas')
    else:
        return redirect('lista_mascotas')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Persona, Mascota, Adopcion
from django.db import IntegrityError


# LISTAR ADOPCIONES
def listaAdopciones(request):
    adopciones = Adopcion.objects.all()
    return render(request, "adopciones/lista.html", {'Adopciones': adopciones})


# CREAR NUEVA ADOPCION
def nuevaAdopcion(request):
    personas = Persona.objects.all()
    mascotas = Mascota.objects.all()
    return render(request, "adopciones/crear.html", {'Personas': personas, 'Mascotas': mascotas})

# GUARDAR NUEVA ADOPCION
def guardarAdopcion(request):
    if request.method == "POST":
        persona_id = request.POST['persona']
        mascota_id = request.POST['mascota']
        observaciones = request.POST.get('observaciones', '')

        persona = Persona.objects.get(id=persona_id)
        mascota = Mascota.objects.get(id=mascota_id)

        # Verificar disponibilidad
        if mascota.estado != 'Disponible':
            messages.error(request, "La mascota ya ha sido adoptada")
            return redirect('crear_adopcion')

        # Crear adopción
        Adopcion.objects.create(
            persona=persona,
            mascota=mascota,
            observaciones=observaciones
        )

        # Cambiar estado de la mascota
        mascota.estado = 'Adoptado'
        mascota.save()

        messages.success(request, "Adopción registrada exitosamente")
        return redirect('lista_adopciones')
    else:
        return redirect('crear_adopcion')


# EDITAR ADOPCION
def editarAdopcion(request, id):
    adopcionEditar = Adopcion.objects.get(id=id)
    personas = Persona.objects.all()
    mascotas = Mascota.objects.all()
    return render(request, "adopciones/editar.html", {
        'adopcionEditar': adopcionEditar,
        'Personas': personas,
        'Mascotas': mascotas
    })


# ACTUALIZAR ADOPCION
def actualizarAdopcion(request):
    if request.method == "POST":
        id = request.POST['id']
        persona_id = request.POST['persona']
        mascota_id = request.POST['mascota']
        observaciones = request.POST.get('observaciones', '')

        adopcion = Adopcion.objects.get(id=id)
        nueva_persona = Persona.objects.get(id=persona_id)
        nueva_mascota = Mascota.objects.get(id=mascota_id)
        mascota_anterior = adopcion.mascota

        # Restaurar estado de mascota anterior
        mascota_anterior.estado = 'Disponible'
        mascota_anterior.save()

        # Verificar disponibilidad de la nueva mascota
        if nueva_mascota.estado != 'Disponible':
            messages.error(request, "La mascota seleccionada ya ha sido adoptada")
            return redirect('editar_adopcion', id=id)

        # Actualizar adopción
        adopcion.persona = nueva_persona
        adopcion.mascota = nueva_mascota
        adopcion.observaciones = observaciones
        adopcion.save()

        # Cambiar estado de la nueva mascota
        nueva_mascota.estado = 'Adoptado'
        nueva_mascota.save()

        messages.success(request, "Adopción actualizada exitosamente")
        return redirect('lista_adopciones')
    else:
        return redirect('lista_adopciones')


# ELIMINAR ADOPCION
def eliminarAdopcion(request, id):
    adopcion = Adopcion.objects.get(id=id)
    mascota = adopcion.mascota

    adopcion.delete()

    # Restaurar estado de la mascota
    mascota.estado = 'Disponible'
    mascota.save()

    messages.success(request, "Adopción eliminada y estado de mascota actualizado")
    return redirect('lista_adopciones')
