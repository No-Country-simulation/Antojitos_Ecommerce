from django.shortcuts import render


# Create your views here.
from carrito.carrito import Carrito
from productos.models import Producto

from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def update_productos(request):

    if request.method == 'POST':

        try:
            # recupera valores del widget_carrito.js
            producto_id = int(request.POST.get('producto_id'))
            action = request.POST.get('action')
            value = int(request.POST.get('value'))

            # Recuperar carrito de la sesión del usuario
            carrito = Carrito(request)

            if action == 'add':
                # realiza la consulta en la SQL con get y devuelve el producto o un error segun corresponda
                producto = get_object_or_404(Producto, id=producto_id)
                # producto = Producto.objects.get(id=producto_id)
                carrito.add_producto(producto, value)
                mensaje = 'Producto agregado'

            elif action == 'less':
                carrito.less_producto(producto_id=producto_id)
                mensaje = 'Producto reducido'

            elif action == 'remove':
                carrito.remove_producto(producto_id=producto_id)
                mensaje = 'Producto eliminado'

            else:
                return JsonResponse({'error': 'Acción inválida'}, status=400)

            cart_items = []
            total_cantidad = 0

            for key, item in carrito.items:
                # Agregar cada item al listado cart_items
                cart_items.append({
                    'id': item['id'],
                    'nombre': item['nombre'],
                    'cantidad': item['cantidad'],
                    'precio': item['precio'],
                    'imagen': item['imagen']
                })

                # Suma de la cantidad de items unicos y repetidos
                total_cantidad += item['cantidad']

            """ 
            cart_items = [{'id': item['id'],
                           'nombre': item['nombre'],
                           'cantidad': item['cantidad'],
                           'precio': item['precio'],
                           'imagen': item['imagen']} for key, item in carrito.items]
            """

            # mensaje: es de depuración
            # carrito.total: llama a la propiedad del models Carrito actualizando su valor según corresponda
            # cart_items: es un array que recupera todos los datos del carrito para mostrarlos sin recargar la pagina

            return JsonResponse({'mensaje': mensaje,
                                 'total': carrito.total,
                                 'cant_total': total_cantidad,
                                 'items': cart_items})

        # cuando no exista el id en el carrito
        except ValueError:
            return JsonResponse({'error': 'ID de producto inválido'}, status=400)

    return JsonResponse({'error': 'Solicitud inválida'}, status=400)


def ver_carrito(request):
    """
        Esta función solo sirve para visualizar el carrito, no necesita de un contexto ya que el
        "carrito" se actualiza de por si en  cada accion y es un context_processors.
    """
    return render(request, "carrito/ver_carrito.html")