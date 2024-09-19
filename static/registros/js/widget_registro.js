

// Función para mostrar/ocultar el dropdown
function toggleDropdown() {
    var userButton = document.getElementById("user-button");
    var userDropdownAuth = document.getElementById("user-dropdown-auth");
    var userDropdown = document.getElementById("user-dropdown");

    // Determinar cuál de los dropdowns está presente
    var dropdown = userDropdownAuth ? userDropdownAuth : userDropdown;

    dropdown.classList.toggle("show");
    var expanded = dropdown.classList.contains("show");
    userButton.setAttribute("aria-expanded", expanded);
}

// Manejar clic en el botón de usuario y el icono
document.getElementById("user-button").addEventListener("click", toggleDropdown);
document.querySelector(".btn-header i").addEventListener("click", function(event) {
    event.stopPropagation(); // Evitar que el evento se propague al botón
    toggleDropdown();
});

// Cerrar dropdown si se hace clic fuera de él
window.addEventListener("click", function(event) {
    var userDropdownAuth = document.getElementById("user-dropdown-auth");
    var userDropdown = document.getElementById("user-dropdown");
    var userButton = document.getElementById("user-button");

    // Determinar cuál de los dropdowns está presente
    var dropdown = userDropdownAuth ? userDropdownAuth : userDropdown;

    if (!event.target.matches('#user-button') && !event.target.closest('#user-dropdown') &&
        !event.target.closest('#user-dropdown-auth') && dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
        userButton.setAttribute("aria-expanded", "false");
    }
});

// Cerrar dropdown con la tecla Esc
window.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        var userDropdownAuth = document.getElementById("user-dropdown-auth");
        var userDropdown = document.getElementById("user-dropdown");
        var userButton = document.getElementById("user-button");

        // Determinar cuál de los dropdowns está presente
        var dropdown = userDropdownAuth ? userDropdownAuth : userDropdown;

        if (dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
            userButton.setAttribute("aria-expanded", "false");
        }
    }
});
