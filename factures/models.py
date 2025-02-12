from django.db import models
from django.utils.timezone import now
from product.models import ProductPage, ProductVariant


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),  # En attente de paiement
        ("paid", "Payée"),          # Payée
        ("cancelled", "Annulée"),   # Annulée
    ]

    number = models.CharField(max_length=20, unique=True, verbose_name="Numéro de facture")
    billing_address = models.TextField(verbose_name="Adresse de facturation")
    total_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Total HT")
    total_tva = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="TVA")
    total_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Total TTC")
    created_at = models.DateTimeField(default=now, verbose_name="Date de création")
    due_date = models.DateTimeField(verbose_name="Date d'échéance")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending", verbose_name="Statut")
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name="Annulée le")
    cancellation_reason = models.TextField(null=True, blank=True, verbose_name="Raison d'annulation")

    def cancel(self, reason):
        """
        Annule une facture avec justification.
        """
        if self.status == "cancelled":
            raise ValueError("Cette facture est déjà annulée.")
        self.status = "cancelled"
        self.cancelled_at = now()
        self.cancellation_reason = reason
        self.save()

    def generate_pdf(self):
        """
        Génération de facture PDF (Factur-X ou autre).
        """
        from factures.utils.pdf_generator import generate_invoice_pdf
        return generate_invoice_pdf(self)

    def __str__(self):
        return f"Facture {self.number}"


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(ProductPage, null=True, blank=True, on_delete=models.SET_NULL, related_name="invoice_lines")  # Rendre nullable
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL, related_name="invoice_lines")
    description = models.CharField(max_length=255, verbose_name="Description")
    unit_price_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire HT")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux de TVA (%)")
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Poids du produit")

    def calculate_ht(self):
        """Calcule le montant HT pour cette ligne"""
        return self.unit_price_ht * self.quantity

    def calculate_tva(self):
        """Calcule la TVA pour cette ligne"""
        return self.calculate_ht() * (self.tax_rate / 100)

    def calculate_ttc(self):
        """Calcule le montant TTC pour cette ligne"""
        return self.calculate_ht() + self.calculate_tva()

    def __str__(self):
        return f"{self.product.title if self.product else 'Produit inconnu'} x {self.quantity}"
