from django.shortcuts import render
from productos.models import Producto, Categoria

def obtener_productos_por_categoria(categorias):
    """Devuelve un diccionario con categorías como llaves y productos asociados como valores."""
    productos_por_categoria = {}
    
    for categoria in categorias:
        productos_por_categoria[categoria.nombre] = Producto.objects.filter(category=categoria)
    
    return productos_por_categoria

def producto(request):
    # Obtén todos los productos y categorías
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    # Obtén categorías únicas desde los productos
    categorias_unicas = Categoria.objects.filter(producto__in=productos).distinct()
    
    # Obtén productos por categorías usando la función auxiliar
    productos_por_categoria = obtener_productos_por_categoria(categorias_unicas)
    
    contexto = {
        "productos": productos,
        "categorias": categorias,
        "productos_por_categoria": productos_por_categoria,
       ## **productos_por_categoria,  # Desempaqueta el diccionario de productos por categoría
    }
    
    return render(request, "productos/producto.html", contexto)

   



