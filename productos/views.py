from django.shortcuts import render

# Create your views here.
from productos.models import Producto



def producto(request):

    # Obtengo todos los productos de la DB Este es el return por defecto cuando accedemos al tab "Producto"
    qs_products = Producto.objects.all()
    contexto = {"productos": qs_products}     # None
    
    return render(request, "productos/producto.html", contexto)






