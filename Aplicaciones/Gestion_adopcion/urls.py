from django.urls import path
from . import views

urlpatterns = [
    # Personas
    path('', views.listaPersonas, name='lista_personas'),
    path('personas/crear/', views.nuevaPersona, name='crear_persona'),
    path('personas/guardar/', views.guardarPersona, name='guardar_persona'),
    path('personas/editar/<int:id>/', views.editarPersona, name='editar_persona'),
    path('personas/eliminar/<int:id>/', views.eliminarPersona, name='eliminar_persona'),
    path('personas/actualizar/', views.procesarEdicionPersona, name='actualizar_persona'),
    
    # Mascotas
    path('mascotas/', views.listaMascotas, name='lista_mascotas'),
    path('mascotas/crear/', views.nuevaMascota, name='crear_mascota'),
    path('mascotas/guardar/', views.guardarMascota, name='guardar_mascota'),
    path('mascotas/editar/<int:id>/', views.editarMascota, name='editar_mascota'),
    path('mascotas/eliminar/<int:id>/', views.eliminarMascota, name='eliminar_mascota'),
    path('mascotas/actualizar/', views.procesarEdicionMascota, name='actualizar_mascota'),

    # Adopciones
    path('adopciones/', views.listaAdopciones, name='lista_adopciones'),
    path('adopciones/crear/', views.nuevaAdopcion, name='crear_adopcion'),
    path('adopciones/guardar/', views.guardarAdopcion, name='guardar_adopcion'),
    path('adopciones/editar/<int:id>/', views.editarAdopcion, name='editar_adopcion'),
    path('adopciones/actualizar/', views.actualizarAdopcion, name='actualizar_adopcion'),
    path('adopciones/eliminar/<int:id>/', views.eliminarAdopcion, name='eliminar_adopcion'),

    # Reportes
    path('reportes/', views.reportes, name='reportes'),

]
