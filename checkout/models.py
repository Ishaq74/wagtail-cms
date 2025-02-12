from django import forms
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.admin.forms import WagtailAdminModelForm
from django.conf import settings
from wagtail import blocks
from wagtail.fields import StreamField
from streams.blocks import OpeningHoursBlock

@register_setting
class CheckoutSettings(BaseGenericSetting):
    store_name = models.CharField(max_length=255, default="Mon Magasin")
    currency = models.CharField(max_length=10, default="EUR", help_text="Devise (ex : EUR, USD)")
    daily_exchange_rate = models.BooleanField(default=True, help_text="Activer la conversion quotidienne. Mensuel par défault.")
    tax_rate_default = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, help_text="Taxe en % par défaut")
    enable_delivery = models.BooleanField(default=True, help_text="Activer livraison")
    enable_pickup = models.BooleanField(default=True, help_text="Activer emport")
    enable_stripe = models.BooleanField(default=True, help_text="Activer Stripe")
    enable_cod = models.BooleanField(default=True, help_text="Activer Paiement à la livraison (COD)")
    stripe_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="Clé API secrète de Stripe")
    stripe_publishable_key = models.CharField(max_length=255, blank=True, null=True, help_text="Clé publique de Stripe")
    enable_email_notifications = models.BooleanField(default=False, help_text="Activer les notifications par email")
    email_subject = models.CharField(max_length=255, default="Confirmation de commande", help_text="Sujet de l'email de confirmation")
    email_body_template = RichTextField(
        default="Merci pour votre commande #{order_id}. Total : {total} {currency}.",
        help_text="Modèle d'email de confirmation. Utilisez {order_id}, {total}, {currency} pour les informations.",
        features=['bold', 'italic', 'link', 'code', 'h1', 'h2', 'h3'],
    )
    opening_hours = StreamField([
        ('opening_hours', OpeningHoursBlock())
    ], blank=True, use_json_field=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("store_name"),
            FieldPanel("currency"),
            FieldPanel("daily_exchange_rate"),
            FieldPanel("tax_rate_default"),
            FieldPanel("enable_delivery"),
            FieldPanel("enable_pickup"),
            FieldPanel("enable_stripe"),
            FieldPanel("stripe_api_key"),
            FieldPanel("stripe_publishable_key"),
            FieldPanel("enable_cod"),
            FieldPanel("opening_hours"),
        ], heading="Configuration du magasin"),

        MultiFieldPanel([
            FieldPanel("email_subject"),
            FieldPanel("email_body_template"),
            FieldPanel("enable_email_notifications"),
        ], heading="Paramètres et contenu des emails"),
    ]

    def __str__(self):
        return self.store_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Commandé'),
        ('paid', 'Payé'),
        ('ready', 'Prêt'),
        ('shipped', 'Expédié'),
        ('delivered', 'Livré'),
        ('canceled', 'Annulé')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('Stripe', 'Stripe'),
            ('COD', 'Paiement à la livraison')
        ]
    )
    delivery_option = models.CharField(
        max_length=10,
        choices=[
            ('delivery', 'Livraison'),
            ('pickup', 'Emport')
        ]
    )
    delivery_address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ordered'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID du PaymentIntent Stripe"
    )


    panels = [
        FieldPanel('user'),
        FieldPanel('total_amount'),
        FieldPanel('payment_method'),
        FieldPanel('delivery_option'),
        FieldPanel('delivery_address'),
        FieldPanel('phone_number'),
        FieldPanel('email'),
        FieldPanel('status'),
    ]

    class Meta:
        ordering = ['-date_created']  # Tri par date de création décroissante

    def __str__(self):
        return f"Commande #{self.id} - {self.get_status_display()} - Total: {self.total_amount}€"

    def update_status(self, new_status):
        self.status = new_status
        self.save()