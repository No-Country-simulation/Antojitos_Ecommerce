
let isSwitchingModal = false; // Variable de control para manejar el cambio de modales

document.getElementById('openPagoTarjeta').addEventListener('click', function () {
    isSwitchingModal = true; // Indicamos que estamos cambiando de modal

    // Cerrar la primera modal (modalPago)
    var modalPago = new bootstrap.Modal(document.getElementById('modalPago'));
    modalPago.hide();

    // Mostrar la segunda modal (pagoTarjeta)
    var pagoTarjeta = new bootstrap.Modal(document.getElementById('pagoTarjeta'));
    pagoTarjeta.show();

    // Reabrir la primera modal cuando se cierre la segunda
    document.getElementById('pagoTarjeta').addEventListener('hidden.bs.modal', function () {
        if (isSwitchingModal) {
            modalPago.show(); // Solo mostrar la primera modal si estamos en el proceso de cambio
        }
        isSwitchingModal = false; // Resetear la variable de control
    });
});

// Desactivar la reapertura de la primera modal cuando se cierra normalmente
document.getElementById('modalPago').addEventListener('hidden.bs.modal', function () {
    isSwitchingModal = false; // Resetear la variable de control al cerrar la primera modal
});

// Asegurar que al cerrar completamente las modales, el fondo gris desaparezca
document.querySelectorAll('.modal').forEach(function(modalElement) {
    modalElement.addEventListener('hidden.bs.modal', function() {
        if (document.querySelectorAll('.modal.show').length === 0) {
            document.body.classList.remove('modal-open'); // Remover la clase que deja el fondo gris
            document.querySelector('.modal-backdrop')?.remove(); // Eliminar el backdrop si queda
        }
    });
});
