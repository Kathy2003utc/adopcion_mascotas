from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Persona, Mascota, Adopcion
from django.db import IntegrityError
from django.db.models import Count

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
        edad_valor = request.POST.get('edad_valor', '')
        edad_unidad = request.POST.get('edad_unidad', '')
        sexo = request.POST['sexo']
        descripcion = request.POST.get('descripcion', '')
        foto = request.FILES.get('foto', None)

        if not edad_valor or not edad_unidad:
            messages.error(request, "Debe ingresar la edad y la unidad.")
            return redirect('crear_mascota')

        Mascota.objects.create(
            nombre=nombre,
            especie=especie,
            raza=raza,
            edad_valor=edad_valor,
            edad_unidad=edad_unidad,
            sexo=sexo,
            descripcion=descripcion,
            estado='Disponible',
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
        edad_valor = request.POST.get('edad_valor', '')
        edad_unidad = request.POST.get('edad_unidad', '')
        sexo = request.POST['sexo']
        descripcion = request.POST.get('descripcion', '')
        foto = request.FILES.get('foto', None)

        mascota = Mascota.objects.get(id=id)

        if not edad_valor or not edad_unidad:
            messages.error(request, "Debe ingresar la edad y la unidad.")
            return redirect('editar_mascota', id=id)

        mascota.nombre = nombre
        mascota.especie = especie
        mascota.raza = raza
        mascota.edad_valor = edad_valor
        mascota.edad_unidad = edad_unidad
        mascota.sexo = sexo
        mascota.descripcion = descripcion

        if foto:
            mascota.foto = foto

        # Actualiza el estado según si tiene adopción
        if hasattr(mascota, 'adopcion'):
            mascota.estado = 'Adoptado'
        else:
            mascota.estado = 'Disponible'

        mascota.save()
        messages.success(request, "Mascota actualizada exitosamente")
        return redirect('lista_mascotas')
    else:
        return redirect('lista_mascotas')

    
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

        # Verificar si la mascota ya tiene adopción
        if Adopcion.objects.filter(mascota=mascota).exists():
            messages.error(request, "La mascota ya ha sido adoptada.")
            return redirect('crear_adopcion')

        try:
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
        except IntegrityError:
            messages.error(request, "No se pudo registrar la adopción porque la mascota ya tiene una adopción.")
            return redirect('crear_adopcion')
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

        # Verificar si la nueva mascota ya tiene adopción, ignorando la actual
        if nueva_mascota != mascota_anterior and Adopcion.objects.filter(mascota=nueva_mascota).exists():
            messages.error(request, "La mascota seleccionada ya ha sido adoptada")
            return redirect('editar_adopcion', id=id)

        # Restaurar estado de mascota anterior si se cambió
        if nueva_mascota != mascota_anterior:
            mascota_anterior.estado = 'Disponible'
            mascota_anterior.save()

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

def reportes(request):
    # Número de adopciones por persona
    adopciones_persona = Persona.objects.annotate(total_adopciones=Count('adopciones'))
    personas = [f"{p.nombres} {p.apellidos}" for p in adopciones_persona]
    total_adopciones = [p.total_adopciones for p in adopciones_persona]

    # Número de mascotas por estado
    mascotas_estado = Mascota.objects.values('estado').annotate(total=Count('id'))
    estados = [m['estado'] for m in mascotas_estado]
    total_mascotas_estado = [m['total'] for m in mascotas_estado]

    # Número de mascotas por especie
    mascotas_especie = Mascota.objects.values('especie').annotate(total=Count('id'))
    especies = [m['especie'] for m in mascotas_especie]
    total_mascotas_especie = [m['total'] for m in mascotas_especie]

    # Número de adopciones por especie (qué tipo de mascota se adopta más rápido)
    adopciones_especie = Mascota.objects.filter(adopcion__isnull=False) \
        .values('especie') \
        .annotate(total=Count('adopcion')) \
        .order_by('-total')
    especies_adoptadas = [m['especie'] for m in adopciones_especie]
    total_adopciones_especie = [m['total'] for m in adopciones_especie]

    context = {
        'personas': personas,
        'total_adopciones': total_adopciones,
        'estados': estados,
        'total_mascotas_estado': total_mascotas_estado,
        'especies': especies,
        'total_mascotas_especie': total_mascotas_especie,
        'especies_adoptadas': especies_adoptadas,
        'total_adopciones_especie': total_adopciones_especie,
    }
    return render(request, "reportes/dashboard.html", context)
