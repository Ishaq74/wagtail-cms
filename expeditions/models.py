from django.db import models
from django_countries.fields import CountryField


class Carrier(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom du transporteur")
    api_url = models.URLField(max_length=500, verbose_name="URL de l'API", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    logo = models.ImageField(upload_to="carriers/logos/", verbose_name="Logo du transporteur", blank=True, null=True)

    def __str__(self):
        return self.name


class ShippingOption(models.Model):
    DELIVERY_TYPES = [
        ("standard", "Livraison Standard"),
        ("express", "Livraison Express"),
        ("pickup", "Retrait en magasin"),
    ]

    name = models.CharField(max_length=255, verbose_name="Nom du mode de livraison")
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name="shipping_options")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix de base")
    per_kg_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix par kg")
    max_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Poids max (kg)")
    delivery_type = models.CharField(max_length=50, choices=DELIVERY_TYPES, verbose_name="Type de livraison")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    def calculate_shipping_cost(self, weight):
        """
        Calcule le coût d'expédition en fonction du poids.
        """
        if weight > self.max_weight:
            raise ValueError("Le poids excède la limite autorisée pour cette option.")
        return self.base_price + (self.per_kg_price * weight)

    def __str__(self):
        return f"{self.name} - {self.delivery_type}"


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Prénom")
    last_name = models.CharField(max_length=255, verbose_name="Nom")
    phone_number = models.CharField(max_length=20, verbose_name="Numéro de téléphone", blank=True, null=True)
    address_line1 = models.CharField(max_length=255, verbose_name="Adresse Ligne 1")
    address_line2 = models.CharField(max_length=255, verbose_name="Adresse Ligne 2", blank=True, null=True)
    postal_code = models.CharField(max_length=20, verbose_name="Code postal")
    city = models.CharField(max_length=255, verbose_name="Ville")
    region = models.CharField(max_length=255, verbose_name="Région", blank=True, null=True)
    country = CountryField(verbose_name="Pays")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.country}"


class ShippingLabel(models.Model):
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.CASCADE, related_name="labels")
    shipping_address = models.OneToOneField(
        ShippingAddress, on_delete=models.CASCADE, related_name="shipping_label", verbose_name="Adresse d'expédition"
    )
    order_id = models.CharField(max_length=255, verbose_name="ID de commande")
    tracking_number = models.CharField(max_length=255, verbose_name="Numéro de suivi", blank=True, null=True)
    pdf_label = models.FileField(upload_to="shipping_labels/", verbose_name="Bordereau d'expédition", blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="Généré le")

    def __str__(self):
        return f"Bordereau - Commande {self.order_id}"
