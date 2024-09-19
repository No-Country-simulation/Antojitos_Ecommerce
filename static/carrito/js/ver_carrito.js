

/* ==========================================================================================
                    Handle_Function para controlar los distintos eventos
========================================================================================== */
async function handleActionsView(productId, action, value = 1) {
    try {
        const response = await fetch('/carrito/update/', {
            method: 'POST',     // Especifica que el método de la solicitud es POST
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', // Indica el tipo de contenido de los datos enviados
                'X-CSRFToken': getCookie('csrftoken') // Añade el token CSRF a los encabezados para la seguridad
            },
            body: new URLSearchParams({
                'producto_id': productId, // Envía el ID del producto como parte del cuerpo de la solicitud
                'action': action,    // 'add', 'less', 'remove'
                'value': value    // value for quantity
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        // Actualiza la VIEW del carrito con los datos más recientes
        updateCartView(data);

        // Actualiza la vista del WDIGET carrito con los datos más recientes
        updateCart(data);

        // Muestra el carrito y el overlay
        // document.getElementById('cart-container').classList.add('show');
        // document.getElementById('overlay').classList.add('show');

    } catch (error) {
        console.error('Error:', error); // Maneja y muestra cualquier error en la consola
    }
}

/* ==========================================================================================
                    Función para actualizar la vista del carrito
========================================================================================== */
function updateCartView(data) {
    const carritoTotal = document.getElementById('total-cart-view');
    const carritoTotal2 = document.getElementById('total-cart-view2');
    const carritoContent = document.getElementById('cart-view-contenido');

    // Para calcular el precio total formateado
    var precioTotal = formatNumberWithCommas(data.total);
    carritoTotal.textContent = `$${precioTotal}`;
    carritoTotal2.textContent = `$${precioTotal}`;

    carritoContent.innerHTML = ''; // Borra el contenido actual del carrito

    // data.items.forEach(item => {
    data.items.forEach((item, index, array) => {

        // calcula mi precio formateado para cada item como corresponda
        var precioFormateado = formatNumberWithCommas(item.precio);

        const itemHTML = `

            <!-- Verificar si es el último elemento -->
            <tr class="cart-item-view ${index === array.length - 1 ? '' : 'border-bottom'}">

                <!-- Imagen Producto -->
                <td>
                    <a href="#">
                        <img src="${item.imagen}" class="img-sm">
                    </a>
                </td>

                <!-- Nombre Producto -->
                <td>
                    <a href="#" class="product-title-cart"><strong>
                        ${item.nombre}
                    </strong></a>
                </td>

                <!-- Price col-->
                <td>
                    <div><span> $${precioFormateado} </span></div>
                    <div><span class="text-muted">      </span> </div>
                </td>

                <!-- Increment Decrement col-->
                <td>
                    <div class="quantity-container">
                        <button class="btn-quantity" onclick="decrement(this)"
                        id="btn-cart-less-${item.id}">
                            -
                        </button>

                        <input type="text" class="form-control quantity-input"
                               id="quant-cart-${item.id}" value="${item.cantidad}" min="1" readonly>

                        <button class="btn-quantity" onclick="increment(this)"
                        id="btn-cart-plus-${item.id}">
                            +
                        </button>
                    </div>
                </td>

                <!-- Subtotal col-->
                <td>
                    <h5 id="item-price-${item.id}" data-precio="${item.precio}"
                        data-cantidad="${item.cantidad}"></h5>
                </td>

                <!-- Buttons col-->
                <td class="text-right">
                    <button class="btn-cart-view" id="btn-like-cart-${item.id}">
                        <i class="fa fa-heart"></i>
                    </button>
                    <button class="btn-cart-view" id="btn-delete-cart-${item.id}">
                        <i class="fas fa-times"></i>
                    </button>
                </td>
            </tr>
        `;
        carritoContent.innerHTML += itemHTML;
    });

    // Reasignar eventos después de actualizar el carrito
    assignButtonEventsCartView();
    calculeSubTotal();
}

// Se supone que esta funcion ya esta cargada en widget_carrito, asique la voy a comentar
/* function formatNumberWithCommas(number) {
    // Convertir el número a string para trabajar con él
    var parts = number.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    // Unir la parte entera con la parte decimal, si existe
    return parts.join(".");
} */

// esta funcion es para calcular el subtotal para item
// document.addEventListener('DOMContentLoaded', function() {
function calculeSubTotal() {
    // Selecciona todos los elementos con ID que comienzan con 'item-price-'
    document.querySelectorAll('[id^="item-price-"]').forEach(item => {
        // Obtén los valores de precio y cantidad desde los atributos de datos
        const precio = parseFloat(item.getAttribute('data-precio'));
        const cantidad = parseInt(item.getAttribute('data-cantidad'), 10);

        // Calcula el subtotal
        const subtotal = precio * cantidad;

        // Formatea el subtotal sin decimales y con comas como separador de miles
        const formattedSubtotal = subtotal.toLocaleString('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });

        // Asigna el subtotal formateado al contenido del elemento
        item.textContent = formattedSubtotal;
    });
}
/* ==========================================================================================
                    Función para asignar eventos a los botones
========================================================================================== */
function assignButtonEventsCartView() {
    // Reasigna eventos a los botones de incremento
    document.querySelectorAll('[id^="btn-cart-plus-"]').forEach(button => {
        button.addEventListener('click', () => {
            const productoId = button.id.split('-').pop();
            handleActionsView(productoId, 'add');
        });
    });

    // Reasigna eventos a los botones de decremento
    document.querySelectorAll('[id^="btn-cart-less-"]').forEach(button => {
        button.addEventListener('click', () => {
            const productoId = button.id.split('-').pop();
            handleActionsView(productoId, 'less');
        });
    });

    // Obtener todos los id de botones de delete productos
    document.querySelectorAll('[id^="btn-delete-cart-"]').forEach(button => {
        button.addEventListener('click', () => {
            const productoId = button.id.split('-').pop();
            handleActionsView(productoId, 'remove');
            handleRemoveCartView(button.id);
        });
    });
}

// Función para manejar la eliminación del ítem
function handleRemoveCartView(itemId) {
    const item = document.getElementById(itemId).closest('.cart-item-view');
    item.remove();
    // Lógica para eliminar el ítem del carrito alert('Ítem eliminado');
}

// Reasignar eventos después de actualizar el carrito
calculeSubTotal();
assignButtonEventsCartView();



// Función para obtener el valor del cookie por nombre actua como nuestro csrf token
// Esta funcion se aplica en widget_carrito como en add_btn.js de producto js
/*
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Comprueba si el cookie tiene el nombre deseado
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Extrae y decodifica el valor del cookie
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
*/


