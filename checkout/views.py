import subprocess
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, CheckoutSettings
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from cart.models import Cart
import stripe
from smtp.models import SMTPSettings
from django.core.mail import EmailMessage, get_connection
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.template.loader import render_to_string

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
    current_day = localtime().strftime('%A').lower()
    current_time = localtime().time()
    opening_hours = []

    # Charger les horaires d'ouverture depuis le StreamField
    for block in settings_instance.opening_hours:
        opening_hours.append({
            'day': block.value['day'],
            'is_closed': block.value['closed'],
            'open_time': block.value['open_time'],
            'close_time': block.value['close_time'],
            'second_open_time': block.value.get('second_open_time'),
            'second_close_time': block.value.get('second_close_time'),
        })

    is_open = False
    for hours in opening_hours:
        if hours['day'] == current_day:
            if hours['is_closed']:
                break
            if hours['open_time'] <= current_time <= hours['close_time']:
                is_open = True
                break
            if hours['second_open_time'] and hours['second_close_time']:
                if hours['second_open_time'] <= current_time <= hours['second_close_time']:
                    is_open = True
                    break

    if not is_open:
        return render(request, 'checkout/closed.html', {
            'message': "Le magasin est actuellement fermé. Veuillez revenir pendant nos heures d'ouverture.",
            'opening_hours': opening_hours,
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
                'opening_hours': opening_hours,
            })

        if delivery_option == 'delivery' and not address:
            return render(request, 'checkout/checkout.html', {
                'cart': cart,
                'settings_instance': settings_instance,
                'error_message': "L'adresse de livraison est requise pour l'option livraison.",
                'opening_hours': opening_hours,
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
            date_created=localtime()
        )

        # Traitement du paiement
        if payment_method == 'Stripe':
            try:
                stripe.api_key = settings_instance.stripe_api_key
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(cart.total_price * 100),
                    currency=settings_instance.currency.lower(),
                    payment_method_types=['card'],
                    receipt_email=email,
                )
                order.stripe_payment_intent_id = payment_intent['id']
                order.save()
                return render(request, 'checkout/stripe_payment.html', {
                    'client_secret': payment_intent['client_secret'],
                    'order': order,
                })

            except stripe.error.StripeError as e:
                order.status = 'canceled'
                order.save()
                return render(request, 'checkout/payment_error.html', {'error_message': str(e)})

        elif payment_method == 'COD':
            cart.delete()
            return redirect('checkout:order_confirmation', order_id=order.id)

        else:
            order.status = 'canceled'
            order.save()
            return render(request, 'checkout/payment_error.html', {'error_message': "Méthode de paiement invalide."})

    # Si la méthode est GET
    return render(request, 'checkout/checkout.html', {
        'cart': cart,
        'settings_instance': settings_instance,
        'opening_hours': opening_hours,
    })


from bs4 import BeautifulSoup

def clean_rich_text(template):
    """Nettoyer les balises HTML inutiles pour éviter les erreurs."""
    soup = BeautifulSoup(template, "html.parser")
    return soup.get_text()

def compile_mjml(mjml_content):
    """Compile MJML en HTML via la commande mjml"""
    try:
        result = subprocess.run(
            ['mjml', '-'],  # MJML prend l'entrée standard
            input=mjml_content,  # Envoie le MJML en entrée
            text=True,  # Assure que l'entrée est traitée comme du texte
            capture_output=True,  # Capture la sortie standard
            check=True  # Lève une exception si la commande échoue
        )
        return result.stdout  # Retourne le HTML compilé
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la conversion MJML en HTML : {e.stderr}")
        return None

def send_order_email(order, settings_instance):
    """Envoi de l'email de confirmation de commande avec MJML"""
    from site_settings.models import OrganisationSettings
    organisation_settings = OrganisationSettings.objects.first()
    if not organisation_settings:
        return False, "Les informations de l'organisation ne sont pas configurées."

    # Préparer les données de contexte pour le modèle MJML
    context = {
        'store_name': settings_instance.store_name,
        'order_id': order.id,
        'total': order.total_amount,
        'currency': settings_instance.currency,
        'payment_method': order.payment_method,
        'delivery_option': order.delivery_option,
        'delivery_address': order.delivery_address or '',  # Adresse de livraison
        'user_name': order.user.username if order.user else '',
        'order_date': order.date_created.strftime('%d/%m/%Y à %H:%M'),
        'organisation_nom': organisation_settings.nom_entreprise,
        'organisation_adresse_rue': organisation_settings.adresse_rue,
        'organisation_adresse_code_postal': organisation_settings.adresse_code_postal,
        'organisation_adresse_ville': organisation_settings.adresse_ville,
        'organisation_adresse_pays': organisation_settings.adresse_pays,
    }

    # Charger le modèle MJML et le rendre avec les données
    mjml_content = render_to_string('checkout/order_confirmation_email.mjml', context)

    # Debug - Assurez-vous que le MJML est correctement rendu
    print(f"Rendered MJML: {mjml_content}")

    # Convertir le MJML en HTML
    html_content = compile_mjml(mjml_content)
    if not html_content:
        return False, "Erreur lors de la compilation du MJML."

    # Envoi de l'email (reste inchangé)
    try:
        smtp_settings = SMTPSettings.objects.first()
        if not smtp_settings:
            return False, "Les paramètres SMTP ne sont pas configurés."

        email = EmailMessage(
            subject=settings_instance.email_subject,
            body=html_content,  # Le corps du message est en HTML
            from_email=smtp_settings.email_host_user,
            to=[order.email],
            connection=get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=smtp_settings.email_host,
                port=smtp_settings.email_port,
                username=smtp_settings.email_host_user,
                password=smtp_settings.decrypt_password(),
                use_tls=smtp_settings.use_tls,
                fail_silently=False,
            ),
        )

        # Assurez-vous que l'email est envoyé avec un encodage UTF-8
        email.content_subtype = "html"  # Indique que l'email est en HTML
        email.charset = 'utf-8'  # Définir l'encodage à UTF-8

        sent_count = email.send(fail_silently=False)

        if sent_count == 0:
            error_message = "L'email n'a pas été accepté par le serveur SMTP."
            print(error_message)
            return False, error_message

        print("Email envoyé avec succès.")
        return True, "Email envoyé avec succès !"

    except Exception as e:
        error_message = f"Erreur lors de l'envoi de l'email : {e}"
        print(error_message)
        return False, error_message



@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    settings_instance = CheckoutSettings.objects.first()

    email_status = None
    if settings_instance and settings_instance.enable_email_notifications:
        success, message = send_order_email(order, settings_instance)
        email_status = {'success': success, 'message': message}

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
