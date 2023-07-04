
from django.contrib import admin
from django.urls import path
from .views import *




urlpatterns = [
    path('',index,name='IND'),
    path('carrito/',carrito,name='CAR'),
    path('categoria/<id>/',categoria,name='CAT'),
    path('contacto/',contacto,name='CON'),
    path('formulario/',formulario,name='FOR'),
    path('galeria/',galeria,name='GAL'),
    path('login/',login,name='LOG'),
    path('modificar/<id>/',modificar,name='MOD'),
    path('noticia/<id>/',noticia,name='NOT'),
    path('perfil_periodista/',perfil_periodista,name='PEPE'),
    path('periodista/<user_id>/',periodista,name='PER'),
    path('registro_periodista/',registro_periodista,name='REPE'),
    path('registro/',registro,name='REG'),
    path('tienda/',tienda,name='TIE'),
    path('modificar_noticia/',modificar_noticia,name='MON'),
    path('grabar_galeria/',grabar_galeria,name='GRG'),
    path('eliminar/<id>/',eliminar,name='ELI'),
    path('filtro_categoria/<id>/',filtro_categoria,name='FCA'),
    path('filtro_contenido/',filtro_contenido,name='FCO'),
    path('filtro_periodista/',filtro_periodista,name='FPE'),
    path('cerrar/',cerrar,name='CER'),
    path('agregar/<id_articulo>/',agregar_articulo,name='AGA'),
    path('quitar/<id_articulo>/',quitar_articulo,name='QA'),
    path('vaciar/',vaciar,name='VAC'),
    path('eliminar_arti/<id_articulo>/',eliminar_arti,name='ELIM'),
]
