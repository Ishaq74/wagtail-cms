from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, CheckoutSettings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import EmailMessage, get_connection
from cart.models import Cart
import stripe
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    settings_instance = CheckoutSettings.objects.first()

    if not cart or not cart.items.exists():
        return redirect('cart:cart_detail')

    # Vérifier si la boutique est configurée
    if not settings_instance:
        return render(request, 'checkout/settings_missing.html', {
            'error_message': "Les paramètres de configuration du checkout ne sont pas définis. Veuillez les configurer dans l'interface d'administration."
        })

    # Vérifier si des méthodes de paiement sont activées
    if not any([settings_instance.enable_stripe, settings_instance.enable_cod]):
        return render(request, 'checkout/settings_missing.html', {
            'error_message': "Aucune méthode de paiement n'est configurée. Veuillez contacter l'administrateur."
        })

    # Vérifier si des options de livraison sont activées
    if not any([settings_instance.enable_delivery, settings_instance.enable_pickup]):
        return render(request, 'checkout/settings_missing.html', {
            'error_message': "Aucune option de livraison n'est configurée. Veuillez contacter l'administrateur."
        })

    # Vérifier si la boutique est ouverte
    current_day = timezone.localtime().strftime('%A')
    current_time = timezone.localtime().time()
    opening_hours = settings_instance.opening_hours

    day_hours = opening_hours.get(current_day, {})
    if not day_hours or day_hours.get('is_closed', True):
        return render(request, 'checkout/closed.html', {
            'message': "Le magasin est fermé aujourd'hui.",
            'opening_hours': opening_hours
        })

    # Vérifier les horaires
    is_open = False
    time_slots = day_hours.get('time_slots', [])
    for slot in time_slots:
        start_time = datetime.strptime(slot['start'], '%H:%M').time()
        end_time = datetime.strptime(slot['end'], '%H:%M').time()
        if start_time <= current_time <= end_time:
            is_open = True
            break

    if not is_open:
        return render(request, 'checkout/closed.html', {
            'message': "Le magasin est actuellement fermé. Veuillez revenir pendant nos heures d'ouverture.",
            'opening_hours': opening_hours
        })

    if request.method == "POST":
        address = request.POST.get("address", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        email = request.POST.get("email", request.user.email).strip()
        payment_method = request.POST.get("payment_method", "").strip()
        delivery_option = request.POST.get("delivery_option", "").strip()

        # Validation des champs requis
        if not phone_number or not email or not payment_method or not delivery_option:
            return render(request, 'checkout/checkout.html', {
                'cart': cart,
                'settings_instance': settings_instance,
                'error_message': "Tous les champs sont requis.",
            })

        if delivery_option == 'delivery' and not address:
            return render(request, 'checkout/checkout.html', {
                'cart': cart,
                'settings_instance': settings_instance,
                'error_message': "L'adresse de livraison est requise pour l'option livraison.",
            })

        # Créer la commande
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            payment_method=payment_method,
            delivery_option=delivery_option,
            delivery_address=address if delivery_option == 'delivery' else '',
            phone_number=phone_number,
            email=email,
            status='ordered',
            date_created=timezone.now()
        )

        # Traitement du paiement
        if payment_method == 'Stripe':
            try:
                stripe.api_key = settings_instance.stripe_api_key
                # Créer un PaymentIntent
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(cart.total_price * 100),  # Montant en centimes
                    currency=settings_instance.currency.lower(),
                    payment_method_types=['card'],
                    receipt_email=email,  # Facultatif : pour envoyer un reçu au client
                )
                # Stocker l'ID du PaymentIntent dans la commande
                order.stripe_payment_intent_id = payment_intent['id']
                order.save()

                # Rendre la page avec le formulaire de paiement Stripe
                return render(request, 'checkout/stripe_payment.html', {
                    'client_secret': payment_intent['client_secret'],
                    'order': order,
                    'settings_instance': settings_instance,
                })

            except stripe.error.StripeError as e:
                order.status = 'canceled'
                order.save()
                return render(request, 'checkout/payment_error.html', {'error_message': str(e)})

        elif payment_method == 'COD':
            # La commande reste à 'ordered'
            email_status = None
            if settings_instance.enable_email_notifications:
                success, message = send_order_email(order, settings_instance)
                email_status = {'success': success, 'message': message}
                print(f"Email status in COD: {email_status}")
            else:
                email_status = {'success': False, 'message': "Les notifications par email sont désactivées."}
                print("Email notifications are disabled.")
            cart.delete()
            return render(request, 'checkout/order_confirmation.html', {
                'order': order,
                'email_status': email_status,
                'settings_instance': settings_instance,
            })

        else:
            order.status = 'canceled'
            order.save()
            return render(request, 'checkout/payment_error.html', {'error_message': "Méthode de paiement invalide."})

    # Si la méthode est GET ou si le formulaire n'est pas valide
    return render(request, 'checkout/checkout.html', {
        'cart': cart,
        'settings_instance': settings_instance,
    })

def send_order_email(order, settings_instance):
    print("Envoi de l'email de commande...")
    subject = settings_instance.email_subject

    # Préparer les variables à passer au modèle d'email
    context = {
        'store_name': settings_instance.store_name,
        'order_id': order.id,
        'total': f"{order.total_amount:.2f}",
        'currency': settings_instance.currency,
        'user_name': order.user.username if order.user else '',
        'order_date': order.date_created.strftime('%d/%m/%Y à %H:%M'),
        'payment_method': order.payment_method,
        'delivery_option': order.get_delivery_option_display(),  # Utilisez la méthode ici
        'delivery_address': order.delivery_address or '',
        'phone_number': order.phone_number or '',
        'email': order.email or '',
    }

    # Remplacer les None par des chaînes vides pour éviter les erreurs
    for key, value in context.items():
        if value is None:
            context[key] = ''

    # Créer le corps de l'email en utilisant le modèle et le contexte
    try:
        body = settings_instance.email_body_template.format(**context)
    except KeyError as e:
        missing_key = str(e)
        error_message = f"La clé {missing_key} est manquante dans le contexte pour le modèle d'email."
        print(error_message)
        return False, error_message

    # Le reste de votre code pour envoyer l'email
    # Vérifier que les paramètres SMTP essentiels sont définis
    required_settings = {
        'email_host': settings_instance.email_host,
        'email_port': settings_instance.email_port,
        'email_host_user': settings_instance.email_host_user,
        'email_host_password': settings_instance.email_host_password,
    }

    missing_settings = [key for key, value in required_settings.items() if not value]

    if missing_settings:
        missing_fields = ', '.join(missing_settings)
        error_message = f"Les paramètres SMTP suivants ne sont pas configurés : {missing_fields}"
        print(error_message)
        return False, error_message

    try:
        # Créer une connexion email personnalisée en spécifiant le backend SMTP
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=settings_instance.email_host,
            port=settings_instance.email_port,
            username=settings_instance.email_host_user,
            password=settings_instance.email_host_password,
            use_tls=True,  # Ajustez selon vos besoins
            fail_silently=False,
        )

        # Créer et envoyer l'email
        email = EmailMessage(
            subject,
            body,
            settings_instance.email_host_user,
            [order.email],
            connection=connection,
        )
        email.send(fail_silently=False)
        print("Email envoyé avec succès.")
        return True, "Email envoyé avec succès."
    except Exception as e:
        error_message = f"Erreur lors de l'envoi de l'email : {str(e)}"
        print(error_message)
        return False, error_message

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    settings_instance = CheckoutSettings.objects.first()
    # Récupérer email_status depuis le localStorage via JavaScript
    email_status = None
    return render(request, 'checkout/order_confirmation.html', {
        'order': order,
        'email_status': email_status,
        'settings_instance': settings_instance,
    })

@csrf_exempt
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        data = json.loads(request.body)
        new_status = data.get('status')
        if new_status == 'paid':
            # Mettre à jour le statut de la commande
            order.update_status(new_status)
            # Supprimer le panier de l'utilisateur
            cart = Cart.objects.filter(user=order.user).first()
            if cart:
                cart.delete()
            # Envoyer un email de confirmation si activé
            settings_instance = CheckoutSettings.objects.first()
            email_status = None
            if settings_instance and settings_instance.enable_email_notifications:
                success, message = send_order_email(order, settings_instance)
                email_status = {'success': success, 'message': message}
                print(f"Email status in update_order_status: {email_status}")
            else:
                email_status = {'success': False, 'message': "Les notifications par email sont désactivées."}
                print("Email notifications are disabled.")
            return JsonResponse({'success': True, 'email_status': email_status})
        return JsonResponse({'success': False})
