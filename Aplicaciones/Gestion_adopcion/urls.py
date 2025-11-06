from django.urls import path
from . import views

urlpatterns = [
    # Personas
    path('personas/', views.listaPersonas, name='lista_personas'),
    path('personas/crear/', views.nuevaPersona, name='crear_persona'),
    path('personas/guardar/', views.guardarPersona, name='guardar_persona'),
    path('personas/editar/<int:id>/', views.editarPersona, name='editar_persona'),
    path('personas/eliminar/<int:id>/', views.eliminarPersona, name='eliminar_persona'),
    path('personas/actualizar/', views.procesarEdicionPersona, name='actualizar_persona'),
]
