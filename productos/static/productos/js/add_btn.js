

// Define la función addToCart para manejar la acción
function addToCart(productId) {
    handleActions(productId, 'add');
}

// Asegúrate de que esta función esté disponible globalmente si no estás usando módulos
window.addToCart = addToCart;


// Tomar en cuenta que esta es la forma para refrescar automatico la busqueda ademas de agregar el evento de los
// botones add-buton, tambien la funcion handle_actions viene de widget_carrito.js es por esto que
// casualmente se trae antes el carrito que es js para que ya este cargada la funcion en memoria

$(document).ready(function() {
    // Prevent form submission on Enter key press
    $('#search-form-prod').on('submit', function(e) {
        e.preventDefault();
    });

    let debounceTimer;
    // Update search results in real-time
    $('#search-input-prod').on('input', function() {

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
                success: function(response) {
                    const productsForSubcats = response.products_for_subcats;

                    // Limpiar el contenedor de productos antes de agregar los nuevos
                    $('#cont-section-prod').empty();

                    // Iterar sobre las subcategorías y sus productos
                    for (const [subcategoria, productos] of Object.entries(productsForSubcats)) {

                        // Crear una sección para la subcategoría
                        const subcatSection = $(`
                            <section id="${subcategoria}" class="sub-card-prod-container">
                                <h2>${subcategoria}</h2>
                                <div class="row"></div>
                            </section>
                        `);
                        
                        // Agregar productos a la sección de subcategoría
                        productos.forEach(producto => {
                            const productCard = `
                                <div class="col-4">
                                    <figure class="sub-card-prod-card" onclick="openModal(${producto.id})">
                                        <img src="${producto.image_url}" alt="Imagen de ${producto.name}">
                                        <figcaption>
                                            <h5>${producto.name}</h5>
                                            <div class="sub-card-prod-price">
                                                <span class="precio-tachado">$${producto.price}</span>
                                                <span class="precio-general">$${producto.price}</span>
                                            </div>
                                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                                <p style="margin: 0;"><strong>Retirar en local</strong></p>
                                                <div class="sub-card-prod-rating">
                                                    <span>4.2</span>
                                                    <span class="stars">★</span>
                                                </div>
                                            </div>
                                            <button class="sub-card-prod-addboton" 
                                                onclick="event.stopPropagation(); addToCart(${producto.id});">
                                                <span>Agregar
                                                    <i class="fa-solid fa-cart-shopping"></i>
                                                </span>
                                            </button>
                                        </figcaption>
                                    </figure>
                                </div>
                            `;
                            // Agregar cada producto a la fila de la subcategoría
                            subcatSection.find('.row').append(productCard);
                        });

                        // Añadir la sección completa al contenedor principal
                        $('#cont-section-prod').append(subcatSection);
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Ocurrió un error al obtener los productos:", error);
                }
            });
        }, 300); // Espera 300ms después de que el usuario deja de escribir
    });
});
