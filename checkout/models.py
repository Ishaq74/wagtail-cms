from django import forms
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.admin.forms import WagtailAdminModelForm
from django.conf import settings

@register_setting
class CheckoutSettings(BaseGenericSetting):
    store_name = models.CharField(max_length=255, default="Mon Magasin")
    currency = models.CharField(max_length=10, default="EUR", help_text="Devise (ex : EUR, USD)")
    tax_rate_default = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, help_text="Taxe en % par défaut")
    enable_delivery = models.BooleanField(default=True, help_text="Activer livraison")
    enable_pickup = models.BooleanField(default=True, help_text="Activer emport")
    enable_stripe = models.BooleanField(default=True, help_text="Activer Stripe")
    enable_cod = models.BooleanField(default=True, help_text="Activer Paiement à la livraison (COD)")

    stripe_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="Clé API secrète de Stripe")
    stripe_publishable_key = models.CharField(max_length=255, blank=True, null=True, help_text="Clé publique de Stripe")

    enable_email_notifications = models.BooleanField(default=False, help_text="Activer les notifications par email")
    email_subject = models.CharField(max_length=255, default="Confirmation de commande", help_text="Sujet de l'email de confirmation")
    email_body_template = models.TextField(
        default="Merci pour votre commande #{order_id}. Total : {total} {currency}.",
        help_text="Modèle d'email de confirmation. Utilisez {order_id}, {total}, {currency} pour les informations."
    )
    email_host = models.CharField(max_length=255, blank=True, null=True, help_text="Serveur SMTP pour l'envoi d'emails")
    email_port = models.IntegerField(blank=True, null=True, help_text="Port SMTP")
    email_host_user = models.CharField(max_length=255, blank=True, null=True, help_text="Utilisateur SMTP")
    email_host_password = models.CharField(max_length=255, blank=True, null=True, help_text="Mot de passe SMTP")

    opening_hours = models.JSONField(default=dict, help_text="Horaires d'ouverture et jours fermés du magasin.")

    panels = [
        MultiFieldPanel([
            FieldPanel("store_name"),
            FieldPanel("currency"),
            FieldPanel("tax_rate_default"),
            FieldPanel("enable_delivery"),
            FieldPanel("enable_pickup"),
            FieldPanel("opening_hours"),
        ], heading="Configuration du magasin"),

        MultiFieldPanel([
            FieldPanel("enable_stripe"),
            FieldPanel("stripe_api_key"),
            FieldPanel("stripe_publishable_key"),
            FieldPanel("enable_cod"),
        ], heading="Méthodes de paiement"),

        MultiFieldPanel([
            FieldPanel("enable_email_notifications"),
            FieldPanel("email_subject"),
            FieldPanel("email_body_template"),
            FieldPanel("email_host"),
            FieldPanel("email_port"),
            FieldPanel("email_host_user"),
            FieldPanel("email_host_password", widget=forms.PasswordInput(render_value=True)),
        ], heading="Paramètres et contenu des emails"),
    ]

    def __str__(self):
        return self.store_name

    @classmethod
    def get_edit_handler(cls):
        edit_handler = super().get_edit_handler()

        class CheckoutSettingsForm(WagtailAdminModelForm):
            class Meta:
                model = cls
                fields = '__all__'
                widgets = {
                    'email_host_password': forms.PasswordInput(render_value=True),
                }

        return edit_handler.bind_to(model=cls, form_class=CheckoutSettingsForm)

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

# Définition d'un SnippetViewSet personnalisé pour Order
class OrderViewSet(SnippetViewSet):
    model = Order
    menu_label = "Commandes"
    menu_icon = "list-ul"  # Icône pour le menu (choisissez celle qui vous convient)
    add_to_admin_menu = True
    list_display = ['id', 'user', 'total_amount', 'status', 'date_created']
    list_filter = ['status', 'payment_method', 'delivery_option']
    search_fields = ['id', 'user__username', 'email', 'phone_number']

# Enregistrement du snippet avec le viewset personnalisé
register_snippet(OrderViewSet)