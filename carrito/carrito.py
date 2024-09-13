class Carrito:
    """
    Esta clase maneja el carrito de compras de un usuario utilizando la sesión del request en Django.

    Atributos:
        request: El objeto de solicitud HTTP de Django, utilizado para acceder a la sesión del usuario.
        session: La sesión del usuario, donde se almacenan los datos del carrito.
        carrito: Un diccionario que representa el carrito de compras del usuario.

    """
    def __init__(self, request):
        """
        Inicializa una instancia de la clase Carrito.

        Parámetros:
            request (HttpRequest): El objeto de solicitud HTTP de Django que contiene la sesión del usuario.

        Comportamiento:
            - Obtiene la sesión del usuario a partir del request.
            - Busca el carrito en la sesión. Si no existe, lo inicializa como un diccionario vacío.
            - Guarda el carrito en la sesión para su posterior uso.
        """
        self.request = request
        self.session = request.session

        carrito = self.session.get("carrito")

        if not carrito:
            carrito = self.session["carrito"] = {}

        self.carrito = carrito

    @property
    def total(self):
        """
        Notes:
            - Se añade el atributo self.total para realizar el calculo solo una vez mediante
            el context_processors.py, y despues pasarlo como contexto
        """
        total = 0
        if self.carrito:
            total = sum(item['precio'] * item['cantidad'] for item in self.carrito.values())
        return total

    @property
    def items(self):
        """
        Notes:
            - Recupera los items del diccionario del carrito para eventualmente recorrerlo de forma
            actualizada
        """
        return self.carrito.items()

    # ======================================================================
    #                   ADD n LESS Products
    # ======================================================================
    def add_producto(self, producto, value):
        """
        Agrega un producto al carrito de compras. Si el producto ya está en el carrito, incrementa la cantidad.

        Parámetros:
            producto (Producto): La instancia del producto que se va a agregar al carrito.
        """
        producto_id_str = str(producto.id)  # Convertir el ID del producto a cadena de texto

        # Verifica si el producto no está en el carrito para agregarlo
        if producto_id_str not in self.carrito.keys():

            # Obtiene los datos de cada producto
            self.carrito[producto_id_str] = {
                "id": producto.id,
                "nombre": producto.name,
                "precio": producto.price,
                "imagen": producto.image_url,
                "cantidad": value
            }

        # Si el producto ya está en el carrito solo uno a la cantidad
        else:
            # se puede agregar una variable de comparacion con el stock *************
            self.carrito[producto_id_str]["cantidad"] += value

        self.save()

    def less_producto(self, producto_id):
        producto_id_str = str(producto_id)  # Convertir el ID del producto a cadena de texto

        if self.carrito[producto_id_str]["cantidad"] > 1:
            self.carrito[producto_id_str]["cantidad"] -= 1
        else:
            # Opcionalmente, podemos eliminar el producto si la cantidad llega a 0
            del self.carrito[producto_id_str]

        # guardamos los cambios
        self.save()

    # ======================================================================
    #                   SAVE, CLEAR; DELETE
    # ======================================================================
    def save(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def remove_producto(self, producto_id):
        producto_id_str = str(producto_id)  # Convertir el ID del producto a cadena de texto

        # if producto_id_str in self.carrito:
        del self.carrito[producto_id_str]
        self.save()

    def clear_producto(self):
        # Todavia no tiene uso en el widget
        self.carrito = {}
        self.save()

    def get_total_precio(self):
        return sum(item["precio"] * item["cantidad"] for item in self.carrito.values())

    def get_total_items(self):
        return sum(item["cantidad"] for item in self.carrito.values())
    