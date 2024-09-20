from django.shortcuts import render, get_object_or_404, redirect
from productos.models import Producto, Categoria, Subcategoria
from registros.models import SellerUser, BuyerUser


from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required


def obtener_categorias_y_subcategorias(categorias_unicas) -> dict:
    """
        Devuelve un diccionario con categorías como llaves y una lista de sus subcategorías 
    como valores.
    
    # Ejemplo del diccionario que se genera
    {
        "Electrónica": ["Computadoras", "Teléfonos"],
        "Hogar": ["Muebles", "Decoración"]
    }
    
    # Forma de usar en HTML
    {% for categoria, subcategorias in categorias_y_subcategorias.items %}
        <h2>{{ categoria }}</h2>
        <ul>
            {% for subcategoria in subcategorias %}
                <li>{{ subcategoria.name }}</li> <!-- O el atributo que quieras mostrar -->
            {% endfor %}
        </ul>
    {% endfor %}
    """

    categorias_y_subcategorias = {}
 
    for categoria in categorias_unicas:
        # Accedemos a las subcategorías de cada categoría
        subcategorias = categoria.subcategorias.all()
        # Usar el objeto `categoria` como clave, no solo su nombre
        categorias_y_subcategorias[categoria] = subcategorias
    
    return categorias_y_subcategorias


def obtener_productos_por_subcategoria(productos) -> dict:
    """
    Devuelve un diccionario con subcategorías como llaves y productos asociados como valores.
    
    # Ejemplo del diccionario que se genera
    {
        "Electrónica": [
            {"nombre": "Laptop", "sub_category": "Electrónica"},
            {"nombre": "Televisor", "sub_category": "Electrónica"}
        ],
        "Hogar": [
            {"nombre": "Sofá", "sub_category": "Hogar"},
            {"nombre": "Mesa", "sub_category": "Hogar"}
        ]
    }
    
    # Forma de usar en HTML
    {% for subcategoria, productos in productos_por_subcategoria.items %}
        <h2>{{ subcategoria }}</h2>
        <ul>
            {% for producto in productos %}
                <li>{{ producto.nombre }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
    """
    productos_por_subcategoria = {}
    
    for producto in productos:
        # Accedemos a la subcategoría del producto
        subcategoria = producto.sub_category  
        if subcategoria not in productos_por_subcategoria:
            productos_por_subcategoria[subcategoria] = []
        productos_por_subcategoria[subcategoria].append(producto)
    
    return productos_por_subcategoria



def producto(request, category_id=None, sub_category_id=None, user_id=None):
    """
        Vista que maneja la lista de productos. Filtra productos por búsqueda, 
        categoría y subcategoría.
    """
    # Obtén todos los productos como punto de partida
    productos = Producto.objects.all()
    category_actual = category_id
    sub_category_actual = sub_category_id

    # Filtrado por búsqueda en la barra superior (si se proporciona una consulta)
    query = request.GET.get('top_search', '')
    if query:
        productos = productos.filter(name__icontains=query)
        
    if user_id:
        # Obtener al comprador
        buyer = get_object_or_404(BuyerUser, id=user_id)
        
        # Obtener el producto
        productos = buyer.saved_products.all()

    # Filtrado por categoría
    if category_id:
        category_actual = Categoria.objects.get(id=category_id)
        productos = productos.filter(category=category_actual)

    # Filtrado por subcategoría (si se pasa un sub_category_id)
    if sub_category_id:
        sub_category_actual = Subcategoria.objects.get(id=sub_category_id)
        productos = productos.filter(sub_category=sub_category_actual)

    # Crear un diccionario de productos agrupados por subcategoría
    products_for_subcats = obtener_productos_por_subcategoria(productos)

    # Contexto para el template
    contexto = {
        "productos": productos,
        "products_for_subcats": products_for_subcats,
        "category": category_actual,           # None or ID
        "sub_category": sub_category_actual,   # None or ID
        'query': query                         # None or 'some'
    }

    return render(request, "productos/producto.html", contexto)


def producto_fav_filter(request, user_id=None, store_id=None):
    
    if user_id:
        # Obtener al comprador
        buyer = get_object_or_404(BuyerUser, id=user_id)
        
        # Obtener el producto
        productos = buyer.saved_products.all()
    
        # Crear un diccionario de productos agrupados por subcategoría
        products_for_subcats = obtener_productos_por_subcategoria(productos)
        
        # Contexto para el template
        contexto = {
            "productos": productos,
            "products_for_subcats": products_for_subcats,
        }

        return render(request, "productos/producto.html", contexto)
    

def tienda_vendedor(request, seller_id=None, category_id=None, sub_category_id=None, prod_id=None):
    seller = get_object_or_404(SellerUser, id=seller_id)
    productos = Producto.objects.filter(seller=seller)
    category_actual = category_id
    sub_category_actual = sub_category_id
    

    # Filtrado por categoría
    if category_id:
        category_actual = Categoria.objects.get(id=category_id)
        productos = productos.filter(category=category_actual)

    # Filtrado por subcategoría (si se pasa un sub_category_id)
    if sub_category_id:
        sub_category_actual = Subcategoria.objects.get(id=sub_category_id)
        productos = productos.filter(sub_category=sub_category_actual)
    
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
        "category": category_actual,           # None or ID
        "sub_category": sub_category_actual,           # None or ID
        'products_for_subcats': products_for_subcats,
    }

    return render(request, 'productos/tienda_vendedor.html', context)



# ==========================================================================
#                         NUEVOS AGREGADOS
# ==========================================================================
@login_required
def fav_products(request, prod_id = None):
    
    user = request.user

    # Verificar que el usuario no sea un vendedor
    if user.role == 'seller':
        messages.error(request, 'Los vendedores no pueden agregar productos a favoritos.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Validar si se recibió un producto_id
    if prod_id is None:
        messages.error(request, 'No se ha recibido un ID de producto.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Obtener al comprador
    buyer = get_object_or_404(BuyerUser, id=user.id)
    
    # Obtener el producto
    producto = get_object_or_404(Producto, id=prod_id)

    # Comprobar si el producto ya está en los favoritos del usuario
    if producto in buyer.saved_products.all():
        buyer.saved_products.remove(producto)
        message = 'Producto eliminado de favoritos.'
    else:
        buyer.saved_products.add(producto)
        message = 'Producto añadido a favoritos.'

    # Mostrar el mensaje correspondiente
    messages.success(request, message)
    
    # Redirigir a la página anterior o a una página por defecto
    return redirect(request.META.get('HTTP_REFERER', '/'))
        




def fav_products2(request):

    if request.method == 'POST':

        try:
            # recupera valores del widget_carrito.js
            producto_id = int(request.POST.get('producto_id'))
    
            user = request.user

            # Verificar que el usuario no sea un vendedor
            if user.role == 'seller':
                return JsonResponse({'error': 'Vendedores no pueden agregar productos a favoritos.'}, status=403)
            
            # Validar si se recibió un producto_id
            if producto_id is None:
                return JsonResponse({'error': 'No se recibió ningún producto.'}, status=400)

            producto = get_object_or_404(Producto, id=producto_id)

            # Comprobar si el producto ya está en los favoritos del usuario
            if producto in user.saved_products.all():
                user.saved_products.remove(producto)
                message = 'Producto eliminado de favoritos.'
            else:
                user.saved_products.add(producto)
                message = 'Producto añadido a favoritos.'

            return JsonResponse({'message': message})
              
        except ValueError:
            return JsonResponse({'error': 'ID de producto inválido'}, status=400)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


# ==========================================================================
#                            FOR REAL TIME SEARCH
# ==========================================================================
@require_GET
def search_view(request):
    
    query = request.GET.get('q', '')
    category_id = request.GET.get('category_id', '0')
    subcategory_id = request.GET.get('subcategory_id', '0')
    q_name_search_top = request.GET.get('q_top_search', '0')

    # Filtrar todos los productos
    productos = Producto.objects.all()

    # Filtrar por categoría si category_id no es '0'
    if category_id != '0':
        category_id = int(category_id)
        productos = productos.filter(category=category_id)

    # Filtrar por subcategoría si subcategory_id no es '0'
    if subcategory_id != '0':
        subcategory_id = int(subcategory_id)
        productos = productos.filter(sub_category=subcategory_id)
        
    # Filtrar por q_top_search si es diferente de '0'
    if q_name_search_top != '0':
        productos = productos.filter(name__icontains=q_name_search_top)
        
    # Filtrar por nombre si la consulta tiene 3 o más caracteres
    if len(query) >= 3:
        productos = productos.filter(name__icontains=query)

    # Agrupar productos por subcategoría
    products_for_subcats = get_sub_cat_n_prod_ajax(productos)

    # Devolver la respuesta como JSON para ser manejada con AJAX
    return JsonResponse({'products_for_subcats': products_for_subcats})


def get_sub_cat_n_prod_ajax(productos) -> dict:
    """
    Devuelve un diccionario de productos agrupados por subcategoría para uso en AJAX.
    
    Ejemplo de la estructura del JSON que se devuelve:
    {
        "productos_por_subcategoria": {
            "Electrónica": [
                {
                    "id": 1,
                    "name": "Laptop",
                    "price": 1000,
                    "desc": "High-end laptop",
                    "discount": 10,
                    "tienda": "Best Buy",
                    "image_url": "url_de_imagen_laptop"
                },
                {
                    "id": 2,
                    "name": "Televisor",
                    "price": 800,
                    "desc": "4K Television",
                    "discount": 15,
                    "tienda": "MediaMarkt",
                    "image_url": "url_de_imagen_televisor"
                }
            ],
            "Hogar": [
                {
                    "id": 3,
                    "name": "Sofá",
                    "price": 500,
                    "desc": "Comfortable sofa",
                    "discount": 5,
                    "tienda": "Ikea",
                    "image_url": "url_de_imagen_sofa"
                }
            ]
        }
    }
    """
    productos_por_subcategoria = {}

    for producto in productos:
        # Obtenemos la subcategoría del producto
        subcategoria = producto.sub_category

        # Si la subcategoría no está en el diccionario, añadirla con una lista vacía
        if subcategoria not in productos_por_subcategoria:
            productos_por_subcategoria[subcategoria] = []
        
        # Agregamos el producto a la lista bajo la subcategoría correspondiente
        productos_por_subcategoria[subcategoria].append({
            'id': producto.id,
            'name': producto.name,
            'price': producto.price,
            'desc': producto.description,
            'discount': producto.discount,
            'tienda': producto.seller,
            'image_url': producto.image_url
        })

    return productos_por_subcategoria



""" 
# ========================================================================
#                FUNCIONES VIEJAS
# ========================================================================
def producto_search(request, category_id=None, sub_category_id=None):

    # Esta petición solo ingresa cuando ingresamos algo en el input de la top bar
    query = request.GET.get('top_search', '')
    if query:
        # Filtra los productos según la consulta del top_search_input
        productos = Producto.objects.filter(name__icontains=query)
        categorias = Categoria.objects.all()
    
        # Obtener las categorías únicas desde los productos (si aún las necesitas)
        categorias_unicas = Categoria.objects.filter(producto__in=productos).distinct()
        
        # Crear un diccionario de las categorías presentes con sus respectivas subcategorías
        cat_n_subcats = obtener_categorias_y_subcategorias(categorias_unicas)

        # Crear un diccionario de productos agrupados por subcategoría
        products_for_subcats = obtener_productos_por_subcategoria(productos)
        
        contexto = {
            "productos": productos,
            "cat_n_subcats": cat_n_subcats,
            "products_for_subcats": products_for_subcats,
            ## **productos_por_categoria,  # Desempaqueta el diccionario de productos por categoría
        }
        
        return render(request, "productos/producto.html", contexto)


def obtener_productos_por_categoria(categorias, productos):
    
    #    Devuelve un diccionario con categorías como llaves y productos asociados como valores.
    
    productos_por_categoria = {}
    
    for categoria in categorias:
        productos_por_categoria[categoria.name] = productos.filter(category=categoria)
        
    return productos_por_categoria
"""