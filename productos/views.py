from django.shortcuts import render, get_object_or_404
from productos.models import Producto, Categoria, Subcategoria
from productos.models import SellerUser


def obtener_categorias_y_subcategorias(categorias) -> dict:
    """
        Devuelve un diccionario con categorías como llaves y una lista de sus subcategorías 
    como valores.
    """
    categorias_y_subcategorias = {}
    
    for categoria in categorias:
        # Accedemos a las subcategorías de cada categoría (ajuste de `related_name`)
        subcategorias = categoria.subcategorias.all()  
        categorias_y_subcategorias[categoria.name] = subcategorias
    
    return categorias_y_subcategorias


def obtener_productos_por_subcategoria(productos) -> dict:
    """
    Devuelve un diccionario con subcategorías como llaves y productos asociados como valores.
    """
    productos_por_subcategoria = {}
    
    for producto in productos:
        # Accedemos a la subcategoría del producto
        subcategoria = producto.sub_category  
        if subcategoria not in productos_por_subcategoria:
            productos_por_subcategoria[subcategoria] = []
        productos_por_subcategoria[subcategoria].append(producto)
    
    return productos_por_subcategoria


def tienda_vendedor(request, seller_id=None):
    seller = get_object_or_404(SellerUser, id=seller_id)
    productos = Producto.objects.filter(seller=seller)

    # Obtener las categorías únicas desde los productos (si aún las necesitas)
    categorias_unicas = Categoria.objects.filter(producto__in=productos).distinct()
    
    # Crear un diccionario de las categorías presentes con sus respectivas subcategorías
    cat_n_subcats = obtener_categorias_y_subcategorias(categorias_unicas)

    # Crear un diccionario de productos agrupados por subcategoría
    products_for_subcats = obtener_productos_por_subcategoria(productos)

    context = {
        'store': seller,
        'productos': productos,
        'cat_n_subcats': cat_n_subcats,
        'products_for_subcats': products_for_subcats,
    }

    return render(request, 'productos/tienda_vendedor.html', context)


def producto_search(request, category_id=None, sub_category_id=None):

    # Esta petición solo ingresa cuando ingresamos algo en el input de la top bar
    query = request.GET.get('top_search', '')
    if query:
        # Filtra los productos según la consulta del top_search_input
        productos = Producto.objects.filter(name__icontains=query)
        categorias = Categoria.objects.all()
    
        # Obtén categorías únicas desde los productos
        categorias_unicas = Categoria.objects.filter(producto__in=productos).distinct()
        
        # Obtén productos por categorías usando la función auxiliar
        productos_por_categoria = obtener_productos_por_categoria(categorias_unicas)
        
        contexto = {
            "productos": productos,
            "categorias": categorias,
            "productos_por_categoria": productos_por_categoria
        }
        
        return render(request, "productos/producto_search.html", contexto)


def producto(request):
    # Obtén todos los productos y categorías
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    # Obtén categorías únicas desde los productos
    categorias_unicas = Categoria.objects.filter(producto__in=productos).distinct()
    
    # Obtén productos por categorías usando la función auxiliar
    productos_por_categoria = obtener_productos_por_categoria(categorias_unicas, productos)
    
    contexto = {
        "productos": productos,
        "categorias": categorias,
        "productos_por_categoria": productos_por_categoria,
        ## **productos_por_categoria,  # Desempaqueta el diccionario de productos por categoría
    }
    
    return render(request, "productos/producto.html", contexto)


def obtener_productos_por_categoria(categorias, productos):
    """
        Devuelve un diccionario con categorías como llaves y productos asociados como valores.
    """
    productos_por_categoria = {}
    
    for categoria in categorias:
        productos_por_categoria[categoria.name] = productos.filter(category=categoria)
        
    return productos_por_categoria



