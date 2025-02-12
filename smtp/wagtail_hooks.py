from wagtail import hooks
from wagtail.models import Site
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import SMTPSettings

@hooks.register("register_admin_urls")
def register_smtp_urls():
    """Enregistre les routes pour les actions SMTP."""
    return [
        path("smtp/test-smtp/", test_smtp_action, name="test_smtp"),
        path("smtp/send-test-email/", send_test_email_action, name="send_test_email"),
    ]

def get_default_site():
    """Récupère le site Wagtail par défaut."""
    return Site.objects.get(is_default_site=True)

def test_smtp_action(request):
    """Action pour tester la connexion SMTP."""
    site = get_default_site()
    smtp_settings = SMTPSettings.for_site(site)
    success, message = smtp_settings.test_smtp_connection()
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect("/admin/settings/smtp/smtpsettings/")

def send_test_email_action(request):
    """Action pour envoyer un email de test."""
    site = get_default_site()
    smtp_settings = SMTPSettings.for_site(site)
    success, message = smtp_settings.send_test_email()
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect("/admin/settings/smtp/smtpsettings/")
