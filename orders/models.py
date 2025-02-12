from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.models import LockableMixin, RevisionMixin, PreviewableMixin
from wagtail.admin.panels import FieldPanel, InlinePanel
from product.models import ProductPage, ProductVariant, VariantOption
from devises.models import RateCurrency, Currency
from checkout.models import CheckoutSettings
from taxes.models import TaxMatrice
from expeditions.models import ShippingOption, ShippingLabel, ShippingAddress
from django_countries.fields import CountryField
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def get_default_currency():
    """Récupère la devise par défaut depuis les settings de Django."""
    try:
        return Currency.objects.get(code=settings.DEFAULT_CURRENCY)  # Assurez-vous que cette devise existe
    except AttributeError:
        return None  # Si la devise par défaut n'est pas définie dans settings.py


@register_snippet
class Order(ClusterableModel, LockableMixin, RevisionMixin, PreviewableMixin):
    STATUS_CHOICES = [
        ("draft", "Brouillon"),
        ("confirmed", "Confirmée"),
        ("processing", "En traitement"),
        ("proceed", "Traitée"),
        ("shipped", "Expédiée"),
        ("delivered", "Livrée"),
        ("cancelled", "Annulée"),
    ]
    customer_name = models.CharField(max_length=255, verbose_name="Nom du client")
    email = models.EmailField(verbose_name="Email")
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders", verbose_name="Devise"
    )  # Remplacé par une clé étrangère vers le modèle Currency
    currency_rate = models.DecimalField(
        max_digits=10, decimal_places=6, null=True, blank=True, verbose_name="Taux de change"
    )  # Nouveau champ pour le taux de change
    billing_address = models.TextField(null=True, blank=True, verbose_name="Adresse de facturation")
    shipping_address = models.OneToOneField(
        ShippingAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order",
    )
    local_total_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    local_total_tva = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    local_total_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    foreign_total_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    foreign_total_tva = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    foreign_total_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    shipping_option = models.ForeignKey(
        ShippingOption, on_delete=models.PROTECT, verbose_name="Option d'expédition", null=True, blank=True
    )
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    shipping_label = models.OneToOneField(
        ShippingLabel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order",
    )
    country = CountryField(verbose_name="Pays")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="draft", verbose_name="Statut")
    is_invoiced = models.BooleanField(default=False, verbose_name="Facturée")
    is_payed = models.BooleanField(default=False, verbose_name="Payée")
    created_at = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def get_exchange_rate(self):
        """Récupère le taux de change basé sur la devise et la date de la commande."""
        if not self.currency or not self.order_date:
            return None

        try:
            rate = RateCurrency.objects.filter(
                currency=self.currency, date__lte=self.order_date
            ).order_by('-date').first()
            return rate.rate if rate else None
        except RateCurrency.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        """Override save pour enregistrer le taux de change au moment de la création de la commande."""
        exchange_rate = self.get_exchange_rate()
        if exchange_rate:
            self.currency_rate = exchange_rate
        else:
            self.currency_rate = 1  # Par défaut, si aucun taux n'est trouvé, on utilise 1
        
        super().save(*args, **kwargs)  # Appelle la méthode save d'origine

    def calculate_totals(self):
        """Calcule les totaux en fonction du taux de change."""
        lines = self.lines.all()
        self.local_total_ht = sum(line.calculate_ht() for line in lines)
        self.local_total_tva = sum(line.calculate_tva() for line in lines)
        self.local_total_ttc = self.local_total_ht + self.local_total_tva + self.shipping_cost

        exchange_rate = self.get_exchange_rate()
        if exchange_rate:
            self.foreign_total_ht = self.local_total_ht / exchange_rate
            self.foreign_total_tva = self.local_total_tva / exchange_rate
            self.foreign_total_ttc = self.local_total_ttc / exchange_rate
        else:
            self.foreign_total_ht = self.local_total_ht
            self.foreign_total_tva = self.local_total_tva
            self.foreign_total_ttc = self.local_total_ttc

        self.save()

    def get_total_weight(self):
        return sum(line.weight for line in self.lines.all())
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return f"Commande {self.id} - {self.customer_name}"

    panels = [
        FieldPanel("customer_name"),
        FieldPanel("email"),
        FieldPanel("billing_address"),
        FieldPanel("shipping_address"),
        FieldPanel("currency_rate"),
        FieldPanel("local_total_ht"),
        FieldPanel("local_total_tva"),
        FieldPanel("local_total_ttc"),
        FieldPanel("shipping_option"),
        FieldPanel("shipping_cost"),
        FieldPanel("shipping_label"),
        FieldPanel("country"),
        FieldPanel("status"),
        FieldPanel("is_invoiced"),
        FieldPanel("is_payed"),
        InlinePanel("lines", label="Lignes de commande"),
    ]
    
    def get_preview_template(self, request, preview_mode):
        return "orders/preview.html"

    def get_preview_context(self, request, preview_mode):
        return {"order": self}


class OrderLine(LockableMixin, RevisionMixin, PreviewableMixin, models.Model):
    order = ParentalKey(Order, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(ProductPage, null=True, blank=True, on_delete=models.CASCADE, related_name="order_lines")
    variant_option = models.ManyToManyField(VariantOption, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price_ht = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price_ttc = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)
    tax_rate = models.ForeignKey(TaxMatrice, on_delete=models.SET_NULL, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        """Override save to ensure that OrderLine is saved before manipulating the ManyToMany field."""
        # Enregistrez l'objet pour obtenir un id
        super().save(*args, **kwargs)

        # Maintenant que l'objet a un id, vous pouvez manipuler la relation ManyToMany
        if self.variant_option.exists():
            self.variant_option.set(self.variant_option.all())  # Exemple : Manipulez la relation Many-to-Many
            # Sauvegardez à nouveau pour appliquer les modifications ManyToMany
            super().save(*args, **kwargs)

    def calculate_ht(self):
        """Calcule le prix hors taxe pour cette ligne de commande."""
        return self.unit_price_ht * self.quantity

    def calculate_tva(self):
        """Calcule la TVA pour cette ligne de commande."""
        return (self.calculate_ht() * (self.tax_rate.tax_rate / 100)) if self.tax_rate else 0.0

    def __str__(self):
        return f"{self.product} x {self.quantity}"
