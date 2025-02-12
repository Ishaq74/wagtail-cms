from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from product.models import ProductPage, VariantOption
from checkout.models import Order
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def get_cart(request):
    """
    Récupère le panier associé à l'utilisateur authentifié ou à la session.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        logger.debug(f"Cart fetched for user {request.user.username}: {cart}")
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            logger.debug(f"Session created with session_key: {session_key}")
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        logger.debug(f"Cart fetched for session {session_key}: {cart}")
    return cart

@require_POST
def add_to_cart(request, product_id):
    """
    Ajoute un produit au panier avec les options sélectionnées.
    """
    try:
        cart = get_cart(request)
        product = get_object_or_404(ProductPage, id=product_id)

        # Récupérer les options sélectionnées depuis le formulaire
        selected_option_ids = []
        for key, value in request.POST.items():
            if key.startswith('variant_') and value.isdigit():
                selected_option_ids.append(int(value))

        # Filtrer les options valides
        selected_options = VariantOption.objects.filter(id__in=selected_option_ids)

        if selected_option_ids and not selected_options.exists():
            logger.error(f"Options sélectionnées invalides pour le produit {product_id}.")
            return JsonResponse({
                'success': False,
                'message': 'Options sélectionnées invalides.',
            }, status=400)

        # Vérifier si un CartItem avec le même produit et les mêmes options existe déjà
        cart_items = CartItem.objects.filter(cart=cart, product=product).prefetch_related('selected_options')

        cart_item = None
        selected_option_ids_set = set(selected_options.values_list('id', flat=True))
        for item in cart_items:
            item_option_ids = set(item.selected_options.values_list('id', flat=True))
            if item_option_ids == selected_option_ids_set:
                item.quantity += 1
                item.save()
                cart_item = item
                break

        if not cart_item:
            # Aucun CartItem correspondant trouvé, en créer un nouveau
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
            cart_item.selected_options.set(selected_options)

        logger.debug(f"Product added to cart: {product.title}, Quantity: {cart_item.quantity}")

        return JsonResponse({
            'success': True,
            'message': 'Produit ajouté au panier avec succès !',
            'cart_item_count': cart.items.count(),
            'cart_total': float(cart.total_price),
        })
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout au panier: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'Erreur lors de l\'ajout au panier.',
        }, status=500)

def cart_detail(request):
    """
    Affiche le détail du panier.
    """
    cart = get_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def remove_from_cart(request, item_id):
    """
    Supprime un article du panier.
    """
    try:
        cart = get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        logger.debug(f"Product removed from cart: {cart_item.product.title}")
        return JsonResponse({
            'success': True,
            'message': 'Produit supprimé du panier.',
            'cart_item_count': cart.items.count(),
            'cart_total': float(cart.total_price),
        })
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du produit: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'Erreur lors de la suppression du produit.',
        }, status=500)

@require_POST
def update_cart(request, item_id):
    """
    Met à jour la quantité d'un article dans le panier.
    """
    try:
        cart = get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        logger.debug(f"Cart item updated: {cart_item.product.title}, New Quantity: {cart_item.quantity}")
        return JsonResponse({
            'success': True,
            'message': 'Quantité mise à jour.',
            'cart_item_count': cart.items.count(),
            'cart_total': float(cart.total_price),
        })
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour du panier: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'Erreur lors de la mise à jour du panier.',
        }, status=500)

def get_cart_data(request):
    """
    Renvoie les données du panier au format JSON.
    """
    try:
        cart = get_cart(request)
        items = []
        for item in cart.items.all():
            try:
                options = [f"{option.variant.name}: {option.name}" for option in item.selected_options.all()]
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des options pour l'article {item.id}: {e}")
                options = []
            
            try:
                product_url = item.product.url
            except Exception as e:
                logger.error(f"Erreur lors de la récupération de l'URL du produit {item.product.id}: {e}")
                product_url = '#'

            try:
                # Utilisez 'file.url' au lieu de 'url'
                product_image = item.product.featured_image.file.url if item.product.featured_image else ''
            except Exception as e:
                logger.error(f"Erreur lors de la récupération de l'image du produit {item.product.id}: {e}")
                product_image = ''

            try:
                unit_price = float(item.product.price)
            except Exception as e:
                logger.error(f"Erreur lors de la récupération du prix du produit {item.product.id}: {e}")
                unit_price = 0.0

            try:
                total_price = float(item.total_price)
            except Exception as e:
                logger.error(f"Erreur lors de la récupération du prix total de l'article {item.id}: {e}")
                total_price = 0.0

            items.append({
                'id': item.id,
                'product_title': item.product.title,
                'product_url': product_url,
                'product_image': product_image,
                'unit_price': unit_price,
                'selected_options': options,
                'quantity': item.quantity,
                'total_price': total_price,
            })
        logger.debug(f"Cart Data: {cart.items.count()} items, Total: {cart.total_price}")
        return JsonResponse({
            'success': True,
            'cart_item_count': cart.items.count(),
            'cart_total': float(cart.total_price),
            'items': items,
        })
    except Exception as e:
        logger.error(f"Erreur dans get_cart_data: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'Erreur lors de la récupération des données du panier.',
        }, status=500)

@login_required
def redirect_to_checkout(request):
    cart = get_cart(request)
    if not cart or not cart.items.exists():
        return redirect('cart:cart_detail')
    return redirect('checkout:checkout')