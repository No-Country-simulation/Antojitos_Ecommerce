

from django.urls import path
from carrito import views

# endpoint para realizar los cambios del carrito dinamicamente en la pagina
urlpatterns = [

    path('carrito/update/', views.update_productos, name='update_productos'),
    path('ver-carrito/', views.ver_carrito, name='Ver_Carrito'),
    path('realizar-compra/', views.realizar_compra, name='realizar_compra'),
]