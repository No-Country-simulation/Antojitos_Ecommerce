

// Tomar en cuenta que esta es la forma para refrescar automatico la busqueda ademas de agregar el evento de los
// botones add-buton, tambien la funcion handle_actions viene de widget_carrito.js es por esto que
// casualmente se trae antes el carrito que es js para que ya este cargada la funcion en memoria

// Define la función addToCart para manejar la acción
function addToCart(productId) {
    handleActions(productId, 'add');
}

// Asegúrate de que esta función esté disponible globalmente si no estás usando módulos
window.addToCart = addToCart;

/*
$(document).ready(function() {
    // Prevent form submission on Enter key press
    $('#search-form').on('submit', function(e) {
        e.preventDefault();
    });

    let debounceTimer;
    // Update search results in real-time
    $('#search-input').on('input', function() {

        // Esto fue agregado por copilot en busqueda de mejoras a la busqueda en tiempo real, ya que asi ahorramos
        // solicitudes que enviamos al servidor para responder nuestra peticion
        clearTimeout(debounceTimer);
        const input = $(this); // Guarda una referencia al input
        debounceTimer = setTimeout(function() {

            // Usar .attr() para obtener el valor del atributo
            // Obtener los atributos del side_bar_search
            let query = input.val();
            let cat_id = input.attr('data-cat-id');
            let sub_cat_id = input.attr('data-sub-cat-id');
            let queryTop = input.attr('data-query-top');

            // Si 'queryTop' no existe, asignar un valor por defecto (si 'queryTop' es undefined o null)
            queryTop = queryTop ? queryTop : '0';

            // Verificar y parsear los valores a un ID o a Zero en caso contrario
            cat_id = cat_id ? parseInt(cat_id, 10) : 0;
            sub_cat_id = sub_cat_id ? parseInt(sub_cat_id, 10) : 0;

            $.ajax({
                url: "/search_producto/",
                data: { q: query,
                        category_id: cat_id, // Pasar la categoria como parametro
                        subcategory_id: sub_cat_id, // Pasar la sub categoria como parametro
                        q_top_search: queryTop // Pasar query_top como parametro
                },
                dataType: 'json',
                success: function(data) {
                    console.log(data); // Verifica los datos recibidos
                    const productsCards = $('#search-results'); // obtiene el contenedor de todas las cards
                    productsCards.empty(); // Clear the current content

                    data.results.forEach(function(producto) {
                        const itemHTML = `
                            <div class="col-3 mb-4">
                                <div class="product-card">

                                    <!-- IMAGEN Producto-->
                                    <div class="image-container">
                                        <!-- Recuadro en la esquina con funcionalidad -->
                                        <button class="corner-box" onclick="alert('Botón de la esquina clicado')">
                                            <i class="fas fa-expand-arrows-alt"></i>
                                        </button>

                                        <img src="${producto.imagen}" class="card-img-top" alt="">
                                    </div>

                                    <div class="product-info">
                                        <p>${producto.nombre}</p>
                                        <p style="color: green;"><strong>Disponible</strong></p>
                                        <p><strong>$ ${producto.precio_contado}</strong></p>

                                        <button id="add-to-cart-${producto.id}" class="add-button px-lg-3">Agregar</button>
                                    </div>

                                </div>
                            </div>
                        `;

                        productsCards.append(itemHTML);
                    });
                },
                error: function(xhr, status, error) {
                    console.log("Error:", status, error);
                }
            });
        }, 300); // Espera 300ms después de que el usuario deja de escribir
    });

    // Delegación de eventos para los botones de agregar al carrito
    // Recordar que hanldeActiones esta en carrito/widget_carrito.js
    $(document).on('click', '[id^="add-to-cart-"]', function() {
        const productoId = $(this).attr('id').split('-').pop();
        handleActions(productoId, 'add');
    });
});

*/

