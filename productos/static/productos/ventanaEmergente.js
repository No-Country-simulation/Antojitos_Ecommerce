

/* 
document.addEventListener('DOMContentLoaded', function() {
    // Función para abrir modal
    function openModal(productId) {
        const modal = document.getElementById(`modal-${productId}`);
        modal.style.display = 'flex';
    }

    // Funciones para manejar la cantidad
    document.querySelectorAll('.quantity-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.id.split('-')[1]; // Extraer el ID del producto
            const quantityDisplay = document.getElementById(`quantityDisplay-${productId}`);
            let currentQuantity = parseInt(quantityDisplay.textContent);
            
            if (this.id.startsWith('decreaseBtn') && currentQuantity > 1) {
                currentQuantity--;
            } else if (this.id.startsWith('increaseBtn')) {
                currentQuantity++;
            }

            quantityDisplay.textContent = currentQuantity;
            const priceElement = document.getElementById(`priceDisplay-${productId}`);
            priceElement.textContent = (currentQuantity * parseFloat(priceElement.dataset.price)).toFixed(2) + ' $';
        });
    });

    // Cerrar la modal cuando se hace clic en el botón de cerrar
    document.querySelectorAll('.close-btn').forEach(function(closeBtn) {
        closeBtn.addEventListener('click', function() {
            const modal = closeBtn.closest('.modal');
            modal.style.display = 'none'; // Ocultar la modal
        });
    });

    // Cerrar la modal cuando se hace clic fuera del contenido de la modal
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none'; // Ocultar la modal
        }
    };

    // Lógica de agregar al carrito
    document.querySelectorAll('.openboton').forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation(); // Evitar que el clic en el botón propague al figure
            // Lógica de agregar al carrito
        });
    });
});
*/


function openModal(productId) {
    const modal = document.getElementById(`modal-${productId}`);
    modal.style.display = 'flex'; // Mostrar la modal específica
}

// Cerrar la modal cuando se hace clic en el botón de cerrar
document.querySelectorAll('.close-btn').forEach(function(closeBtn) {
    closeBtn.addEventListener('click', function() {
        const modal = closeBtn.closest('.modal');
        modal.style.display = 'none'; // Ocultar la modal
    });
});

// Cerrar la modal cuando se hace clic fuera del contenido de la modal
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none'; // Ocultar la modal
    }
};

// Lógica de agregar al carrito
document.querySelectorAll('.openboton').forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation(); // Evitar que el clic en el botón propague al figure
        // Lógica de agregar al carrito
    });
}); 