from django.urls import path

from productos import views

# Esto es para supportear las imagenes de esta app
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # If you want dont pass any parameters in the url you can use this "name"
    path('productos/', views.producto, name="Producto"),  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


