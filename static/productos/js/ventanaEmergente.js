
// Función para abrir la modal usando Bootstrap 5
function openModal(productId) {
    const modal = new bootstrap.Modal(document.getElementById(`modal-${productId}`));
    modal.show(); // Mostrar la modal con Bootstrap 5
}

// Cerrar la modal con Bootstrap se gestiona automáticamente al hacer clic fuera o con el botón de cerrar




// Lógica de agregar al carrito
document.querySelectorAll('.openboton').forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation(); // Evitar que el clic en el botón propague al figure
        // Lógica de agregar al carrito
    });
}); 
