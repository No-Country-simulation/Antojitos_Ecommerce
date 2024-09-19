// Función para abrir la modal usando Bootstrap 5
function openModal(productId) {
    const modal = new bootstrap.Modal(document.getElementById(`modal-${productId}`));
    modal.show(); // Mostrar la modal con Bootstrap 5
}

// Inicializar el carrito y el total
let cart = [];
let total = 0;

// Lógica para manejar el aumento y la disminución de cantidad en el modal
document.querySelectorAll('.quantity-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        const productId = this.id.split('-')[1]; // Obtener el ID del producto del botón

        // Identificar si es el botón de aumentar o disminuir
        const action = this.id.startsWith('increaseBtn') ? 'increase' : 'decrease';
        const quantityDisplay = document.getElementById(`quantityDisplay-${productId}`);
        let currentQuantity = parseInt(quantityDisplay.textContent);

        // Actualizar la cantidad
        if (action === 'increase') {
            currentQuantity++;
        } else if (action === 'decrease' && currentQuantity > 1) {
            currentQuantity--; // Evitar que la cantidad sea menor que 1
        }

        // Reflejar la cantidad en el modal
        quantityDisplay.textContent = currentQuantity;

        // Obtener el precio base del producto
        const priceDisplay = document.getElementById(`priceDisplay-${productId}`);
        const basePrice = parseFloat(priceDisplay.getAttribute('data-base-price'));

        // Calcular el nuevo precio en función de la cantidad
        const newPrice = basePrice * currentQuantity;
        priceDisplay.textContent = `${newPrice.toFixed(2)} $`; // Actualizar el precio en la vista
    });
});

// Lógica de agregar al carrito
document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation(); // Evitar que el clic en el botón propague al figure

        // Obtener el ID del producto y su precio actual
        const productId = this.previousElementSibling.id.split('-')[1];
        const productPrice = parseFloat(document.getElementById(`priceDisplay-${productId}`).textContent);
        const productQuantity = parseInt(document.getElementById(`quantityDisplay-${productId}`).textContent);

        // Agregar el producto al carrito con la cantidad seleccionada
        addToCart(productId, productPrice, productQuantity);
    });
});

// Función para agregar productos al carrito
function addToCart(productId, productPrice, productQuantity) {
    // Buscar el producto en el carrito
    let product = cart.find(item => item.id === productId);

    // Si el producto ya está en el carrito, incrementar la cantidad
    if (product) {
        product.quantity += productQuantity;
    } else {
        // Si el producto no está en el carrito, agregarlo con la cantidad seleccionada
        cart.push({ id: productId, price: productPrice, quantity: productQuantity });
    }

    // Actualizar la visualización del carrito
    updateCart();
}

// Función para actualizar la visualización del carrito
function updateCart() {
    // Obtener el contenedor de items del carrito
    let cartItemsContainer = document.getElementById('cart-items');
    let cartTotal = document.getElementById('cart-total');

    // Limpiar el contenedor de items
    cartItemsContainer.innerHTML = '';

    // Calcular el nuevo total
    total = 0;

    // Iterar sobre los productos en el carrito
    cart.forEach(item => {
        // Crear un nuevo elemento para el producto
        let listItem = document.createElement('li');
        listItem.textContent = `Producto ID: ${item.id}, Cantidad: ${item.quantity}, Precio: $${item.price}`;
        cartItemsContainer.appendChild(listItem);

        // Sumar el precio al total
        total += item.price * item.quantity;
    });

    // Actualizar el total en la vista
    cartTotal.textContent = total.toFixed(2);
}
