from django.db import models
from django.utils.timezone import now
from django_countries.fields import CountryField
from orders.models import Order
from .models import Invoice


class ArchivedOrder(models.Model):
    order_id = models.PositiveIntegerField(verbose_name="ID de la commande originale")
    customer_name = models.CharField(max_length=255, verbose_name="Nom du client")
    email = models.EmailField(verbose_name="Email")
    billing_address = models.TextField(verbose_name="Adresse de facturation")
    shipping_address = models.TextField(verbose_name="Adresse d'expédition", blank=True, null=True)
    total_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total HT")
    total_tva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="TVA")
    total_ttc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total TTC")
    status = models.CharField(max_length=50, verbose_name="Statut")
    archived_at = models.DateTimeField(default=now, verbose_name="Date d'archivage")

    def __str__(self):
        return f"Archive Commande {self.order_id} - {self.customer_name}"


class ArchivedInvoice(models.Model):
    invoice_id = models.PositiveIntegerField(verbose_name="ID de la facture originale")
    order_id = models.PositiveIntegerField(verbose_name="ID de la commande associée")
    customer_name = models.CharField(max_length=255, verbose_name="Nom du client")
    billing_address = models.TextField(verbose_name="Adresse de facturation")
    total_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total HT")
    total_tva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="TVA")
    total_ttc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total TTC")
    is_paid = models.BooleanField(default=False, verbose_name="Payée")
    is_cancelled = models.BooleanField(default=False, verbose_name="Annulée")
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name="Motif d'annulation")
    archived_at = models.DateTimeField(default=now, verbose_name="Date d'archivage")

    def __str__(self):
        return f"Archive Facture {self.invoice_id} - {self.customer_name}"
