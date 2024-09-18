from django.urls import path

from productos import views

# Esto es para supportear las imagenes de esta app
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # If you want dont pass any parameters in the url you can use this "name"
    path('productos/', views.producto, name="Producto"),
    
    # If you want pass 1 parameters in the url you can use this "name"
    path('productos/categoria/<int:category_id>/', views.producto, name="Prod_Cat"),

    # If you want pass 2 parameters in the url you can use this "name"
    path('productos/categoria/<int:category_id>/<int:sub_category_id>/', views.producto, name="Prod_Sub_Cat"),

    # Vista para la barra de busqueda del TOP method GET
    path('productos/search/', views.producto, name="Producto_Search_Top"),
    
    # este trabaja para las solicitudes JSON con js AJAX. para la busqueda en el input lateral del sidebar
    path('search_producto/', views.search_view, name='Search_view'),

    # Para la Vista de Tiendas
    path('tienda/<int:seller_id>/', views.tienda_vendedor, name='Tienda_Profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


