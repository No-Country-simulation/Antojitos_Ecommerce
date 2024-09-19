

/* ==========================================================================================
                   "Función" para Eventos de mostrar y ocultar el carrito
========================================================================================== */
document.getElementById('cart-button').addEventListener('click', function() {
    document.getElementById('cart-container').classList.add('show');
    document.getElementById('overlay').classList.add('show');
});

document.getElementById('close-cart').addEventListener('click', function() {
    document.getElementById('cart-container').classList.remove('show');
    document.getElementById('overlay').classList.remove('show');
});

document.getElementById('overlay').addEventListener('click', function() {
    document.getElementById('cart-container').classList.remove('show');
    document.getElementById('overlay').classList.remove('show');
});

/* ==========================================================================================
                    Handle_Function para controlar los distintos eventos
========================================================================================== */
async function handleActions(productId, action, value = 1) {
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

        // Actualiza la vista del WDIGET carrito con los datos más recientes
        updateCart(data);

        // Muestra el carrito y el overlay
        // Nota por algun motivo esto se tiene que ejecutar antes jeej
        document.getElementById('cart-container').classList.add('show');
        document.getElementById('overlay').classList.add('show');

        // Actualiza la VIEW del carrito con los datos más recientes
        updateCartView(data);

    } catch (error) {
        console.error('Error:', error); // Maneja y muestra cualquier error en la consola
    }
}

/* ==========================================================================================
                    Función para actualizar la vista del carrito
========================================================================================== */
function updateCart(data) {
    const badgeCantTotal = document.getElementById('badge-cart-button');
    const carritoTotal = document.getElementById('carrito-total');
    const carritoContent = document.getElementById('carrito-contenido');

    var precioTotal = formatNumberWithCommas(data.total);
    carritoTotal.textContent = `$${precioTotal}`;

    badgeCantTotal.textContent = `${data.cant_total}`;

    /* carritoTotal.textContent = `Total: $${data.total}`; */
    carritoContent.innerHTML = ''; // Borra el contenido actual del carrito

    data.items.forEach(item => {
        var precioFormateado = formatNumberWithCommas(item.precio);

        const itemHTML = `
            <div class="cart-item position-relative mb-3 d-flex align-items-center">
                <img src="${item.imagen}" class="img-fluid" alt="Product Image">
                <div>
                    <h6>${item.nombre}</h6>
                    <p>${item.cantidad} × $${precioFormateado}</p>
                    <!-- Contador y botón de eliminar -->
                    <div class="d-flex align-items-center">
                        <button class="btn btn-secondary btn-sm" id="decrement-quantity-${item.id}">-</button>
                        <input type="number" class="form-control form-control-sm mx-2" id="quantity-${item.id}" value="${item.cantidad}" min="1" readonly>
                        <button class="btn btn-secondary btn-sm" id="increment-quantity-${item.id}">+</button>
                    </div>
                </div>
                <!-- Botón de eliminar en la esquina superior derecha -->
                <button class="btn btn-danger btn-sm remove-btn" id="remove-item-${item.id}">✖</button>
            </div>
        `;
        carritoContent.innerHTML += itemHTML;
    });

    // Reasignar eventos después de actualizar el carrito
    assignButtonEvents();
}

function formatNumberWithCommas(number) {
    // Convertir el número a string para trabajar con él
    var parts = number.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    // Unir la parte entera con la parte decimal, si existe
    return parts.join(".");
}

/* ==========================================================================================
                    Función para asignar eventos a los botones
========================================================================================== */
function assignButtonEvents() {
    // Reasigna eventos a los botones de incremento
    document.querySelectorAll('[id^="increment-quantity-"]').forEach(button => {
        button.addEventListener('click', () => {
            const productoId = button.id.split('-').pop();
            handleActions(productoId, 'add');
        });
    });

    // Reasigna eventos a los botones de decremento
    document.querySelectorAll('[id^="decrement-quantity-"]').forEach(button => {
        button.addEventListener('click', () => {
            const productoId = button.id.split('-').pop();
            handleActions(productoId, 'less');
        });
    });

    // Obtener todos los id de botones de delete productos
    document.querySelectorAll('[id^="remove-item-"]').forEach(button => {
        button.addEventListener('click', () => {
            const productoId = button.id.split('-').pop();
            handleActions(productoId, 'remove');
            handleRemove(button.id);
        });
    });
}

// Función para manejar la eliminación del ítem
function handleRemove(itemId) {
    const item = document.getElementById(itemId).closest('.cart-item');
    item.remove();
    // Lógica para eliminar el ítem del carrito
    // alert('Ítem eliminado');
}

// Reasignar eventos después de actualizar el carrito
assignButtonEvents();


// Función para obtener el valor del cookie por nombre actua como nuestro csrf token
// Esta funcion se aplica en widget_carrito como en add_btn.js de producto js

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