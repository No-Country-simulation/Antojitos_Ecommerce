

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
        clearTimeout(debounceTimer);
        const input = $(this); // Guarda una referencia al input
        debounceTimer = setTimeout(function() {
            let query = input.val();
            let cat_id = input.attr('data-cat-id');
            let sub_cat_id = input.attr('data-sub-cat-id');
            let queryTop = input.attr('data-query-top');

            queryTop = queryTop ? queryTop : '0';
            cat_id = cat_id ? parseInt(cat_id, 10) : 0;
            sub_cat_id = sub_cat_id ? parseInt(sub_cat_id, 10) : 0;

            $.ajax({
                url: "/search_productos/",
                data: {
                    q: query,
                    category_id: cat_id,
                    subcategory_id: sub_cat_id,
                    q_top_search: queryTop
                },
                dataType: 'json',
                success: function(response) {
                    console.log(response); // Verifica los datos recibidos
                    const productsForSubcats = response.products_for_subcats;

                    // Limpiar el contenedor de productos antes de agregar los nuevos
                    $('#cont-section-prod').empty();

                    // Iterar sobre las subcategorías y sus productos
                    for (const [subcategoria, productos] of Object.entries(productsForSubcats)) {
                        const subcatSection = $(`
                            <section id="${subcategoria}" class="sub-card-prod-container">
                                <h2>${subcategoria}</h2>
                                <div class="row"></div>
                            </section>
                        `);

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
                                            <button class="sub-card-prod-addboton" onclick="event.stopPropagation(); addToCart(${producto.id});">
                                                <span>Agregar
                                                    <i class="fa-solid fa-cart-shopping"></i>
                                                </span>
                                            </button>
                                        </figcaption>
                                    </figure>

                                    <div class="modal fade" id="modal-${producto.id}" tabindex="-1" aria-labelledby="modalLabel-${producto.id}" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h5 class="modal-title" id="modalLabel-${producto.id}">${producto.name}</h5>
                                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div class="modal-body">
                                                    <img src="${producto.image_url}" alt="${producto.name}" class="img-fluid mb-3">
                                                    <p>${producto.description}</p>
                                                    <p><strong>${producto.price} $</strong> <span class="precio-real">${producto.price} $</span></p>
                                                </div>
                                                <div class="modal-footer">
                                                    <div class="d-flex align-items-center">
                                                        <button class="btn btn-outline-secondary quantity-btn" id="decreaseBtn-${producto.id}">-</button>
                                                        <span class="mx-2" id="quantityDisplay-${producto.id}">1</span>
                                                        <button class="btn btn-outline-secondary quantity-btn" id="increaseBtn-${producto.id}">+</button>
                                                        <button class="btn btn-primary ms-3 add-to-cart-btn">
                                                            <img src="carrito.png" alt="" class="me-2">
                                                            <span id="priceDisplay-${producto.id}">${producto.price} $</span>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                            subcatSection.find('.row').append(productCard);
                        });

                        $('#cont-section-prod').append(subcatSection);
                    }

                    // Inicializar los modales
                    $('.modal').modal();

                    // Asignar eventos a los botones de cantidad
                    $('.quantity-btn').off('click').on('click', function() {
                        const productId = $(this).attr('id').split('-')[1];
                        const quantityDisplay = $(`#quantityDisplay-${productId}`);
                        let currentQuantity = parseInt(quantityDisplay.text(), 10);
                        if ($(this).attr('id').startsWith('increase')) {
                            currentQuantity++;
                        } else if ($(this).attr('id').startsWith('decrease') && currentQuantity > 1) {
                            currentQuantity--;
                        }
                        quantityDisplay.text(currentQuantity);
                    });

                    // Asignar eventos al botón de agregar al carrito
                    $('.add-to-cart-btn').off('click').on('click', function() {
                        const productId = $(this).siblings('span').attr('id').split('-')[1];
                        addToCart(productId);
                    });
                }
            });
        }, 300); // Espera 300ms después de que el usuario deja de escribir
    });
});


// Define la función addToCart para manejar la acción
function addToCart(productId) {
    handleActions(productId, 'add');
}

// Asegúrate de que esta función esté disponible globalmente si no estás usando módulos
window.addToCart = addToCart;
