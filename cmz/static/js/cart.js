// static/js/cart.js

document.addEventListener('DOMContentLoaded', function () {
    const cartButton = document.getElementById('cart-button');
    const cartModal = document.getElementById('cart-modal');
    const closeButton = document.querySelector('.close-button');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');
    const cartItemsContainer = document.getElementById('cart-items');

    // Vérifiez si les éléments existent avant d'ajouter des écouteurs
    if (cartButton && cartModal && closeButton && cartCount && cartTotal && cartItemsContainer) {
        // Ouvrir la fenêtre modale
        cartButton.addEventListener('click', function (e) {
            e.preventDefault();
            fetchCartData();
            cartModal.style.display = 'block';
        });

        // Fermer la fenêtre modale
        closeButton.addEventListener('click', function () {
            cartModal.style.display = 'none';
        });

        // Fermer la fenêtre modale en cliquant en dehors
        window.addEventListener('click', function (e) {
            if (e.target == cartModal) {
                cartModal.style.display = 'none';
            }
        });

        // Fermer la modale avec la touche Escape
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                cartModal.style.display = 'none';
            }
        });

        // Focus management
        cartButton.addEventListener('click', function (e) {
            e.preventDefault();
            fetchCartData();
            cartModal.style.display = 'block';
            closeButton.focus();
        });

        closeButton.addEventListener('click', function () {
            cartModal.style.display = 'none';
            cartButton.focus();
        });

        // Gérer les soumissions de formulaires "add-to-cart" via AJAX
        document.querySelectorAll('.add-to-cart-form').forEach(function(form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(form);
                const action = form.action;
                const method = form.method;

                fetch(action, {
                    method: method,
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Add to Cart Response:', data); // Log pour débogage
                    if (data.success) {
                        // Mettre à jour le compteur du panier
                        cartCount.textContent = data.cart_item_count;
                        console.log('Cart Count Updated To:', data.cart_item_count); // Log pour débogage
                        // Animer le compteur
                        cartCount.classList.add('animate-bounce');
                        setTimeout(() => {
                            cartCount.classList.remove('animate-bounce');
                        }, 300);
                        // Afficher la notification toast
                        toastr.success(data.message);
                    } else {
                        toastr.error(data.message);
                    }
                })
                .catch(error => {
                    console.error('Error adding to cart:', error);
                    toastr.error('Erreur lors de l\'ajout au panier.');
                });
            });
        });

        // Fonction pour récupérer les données du panier via AJAX
        function fetchCartData() {
            // Afficher le loader
            cartItemsContainer.innerHTML = '<div class="loader"></div>';

            fetch('/cart/data/')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erreur lors de la récupération des données du panier');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Cart Data:', data); // Log pour débogage
                    if (data.success === false) {
                        throw new Error(data.message || 'Erreur inconnue');
                    }
                    cartCount.textContent = data.cart_item_count;
                    cartTotal.textContent = data.cart_total.toFixed(2);

                    // Animer le compteur
                    cartCount.classList.add('animate-bounce');
                    setTimeout(() => {
                        cartCount.classList.remove('animate-bounce');
                    }, 300);

                    // Afficher la notification toast si un message est présent
                    if (data.message) {
                        toastr.success(data.message);
                    }

                    // Remplir le contenu du panier dans la fenêtre modale
                    let itemsHtml = '';
                    if (data.items.length > 0) {
                        itemsHtml += '<ul>';
                        data.items.forEach(item => {
                            itemsHtml += `
                                <li class="cart-item">
                                    <img src="${item.product_image || '/static/images/default-product.png'}" alt="${item.product_title}" class="cart-item-image">
                                    <div class="cart-item-details">
                                        <a href="${item.product_url}" class="cart-item-title">${item.product_title}</a>
                                        <p>Prix Unitaire: ${item.unit_price} €</p>
                                        ${item.selected_options.length > 0 ? `<p>Options: ${item.selected_options.join(', ')}</p>` : ''}
                                        <p>Quantité: 
                                            <input type="number" value="${item.quantity}" min="1" data-item-id="${item.id}" class="quantity-input">
                                        </p>
                                        <p>Total: ${item.total_price} €</p>
                                        <button class="btn-remove" data-item-id="${item.id}">Supprimer</button>
                                    </div>
                                </li>
                            `;
                        });
                        itemsHtml += '</ul>';
                    } else {
                        itemsHtml = '<p>Votre panier est vide.</p>';
                    }
                    cartItemsContainer.innerHTML = itemsHtml;

                    // Ajouter les événements pour les mises à jour et suppressions
                    document.querySelectorAll('.quantity-input').forEach(input => {
                        input.addEventListener('change', updateCartItem);
                    });

                    document.querySelectorAll('.btn-remove').forEach(button => {
                        button.addEventListener('click', removeCartItem);
                    });
                })
                .catch(error => {
                    console.error('Error fetching cart data:', error);
                    cartItemsContainer.innerHTML = '<p>Impossible de charger le panier. Veuillez réessayer plus tard.</p>';
                    toastr.error('Impossible de charger le panier. Veuillez réessayer plus tard.');
                });
        }

        // Fonction pour mettre à jour la quantité d'un article
        function updateCartItem(e) {
            const itemId = e.target.getAttribute('data-item-id');
            const quantity = e.target.value;

            fetch(`/cart/update/${itemId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `quantity=${quantity}`
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Update Cart Response:', data); // Log pour débogage
                    if (data.success) {
                        fetchCartData();
                    } else {
                        toastr.error('Erreur lors de la mise à jour du panier.');
                    }
                })
                .catch(error => {
                    console.error('Error updating cart item:', error);
                    toastr.error('Erreur lors de la mise à jour du panier.');
                });
        }

        // Fonction pour supprimer un article
        function removeCartItem(e) {
            const itemId = e.target.getAttribute('data-item-id');

            fetch(`/cart/remove/${itemId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Remove Cart Response:', data); // Log pour débogage
                    if (data.success) {
                        fetchCartData();
                    } else {
                        toastr.error('Erreur lors de la suppression du produit.');
                    }
                })
                .catch(error => {
                    console.error('Error removing cart item:', error);
                    toastr.error('Erreur lors de la suppression du produit.');
                });
        }

        // Fonction pour obtenir le token CSRF
        function getCSRFToken() {
            let cookieValue = null;
            const name = 'csrftoken';
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // Initialiser le compteur du panier au chargement de la page
        fetchCartData();
    } else {
        console.warn('Certains éléments du panier sont manquants dans le DOM.');
    }
});
