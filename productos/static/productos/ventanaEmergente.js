const boton = document.getElementById('boton');
const openboton = document.getElementById('openboton');
const closeboton = document.querySelector('.closeboton');

const decreaseBtn = document.getElementById('decreaseBtn');
const increaseBtn = document.getElementById('increaseBtn');
const quantityDisplay = document.getElementById('quantityDisplay');
const priceDisplay = document.getElementById('priceDisplay');

let quantity = 1; // Cantidad inicial de productos
const pricePerItem = 10; // Precio de cada producto

// Abrir la ventana modal
openboton.onclick = function() {
    boton.style.display = 'flex'; // Mostrar la modal
}

// Cerrar la ventana modal cuando se hace clic en el botón de cerrar
closeboton.onclick = function() {
    boton.style.display = 'none'; // Ocultar la modal
}

// Cerrar la ventana modal cuando se hace clic fuera del contenido de la modal
window.onclick = function(event) {
    if (event.target == boton) {
        boton.style.display = 'none'; // Ocultar la modal
    }
}

// Aumentar la cantidad
increaseBtn.onclick = function() {
    quantity++;
    updateDisplay();
}

// Disminuir la cantidad
decreaseBtn.onclick = function() {
    if (quantity > 1) { // No permitir que la cantidad sea menor que 1
        quantity--;
        updateDisplay();
    }
}

// Actualizar la cantidad mostrada y el precio total
function updateDisplay() {
    quantityDisplay.textContent = quantity;
    const totalPrice = (quantity * pricePerItem).toFixed(2);
    priceDisplay.textContent = `${totalPrice} $`;
}
