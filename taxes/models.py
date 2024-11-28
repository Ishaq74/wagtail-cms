from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.models import Site
from .validators import validate_tax_rate, validate_dates

class Country(models.Model):
    iso_code = models.CharField(max_length=2, unique=True, verbose_name="Code ISO")
    name = models.CharField(max_length=100, verbose_name="Nom du pays")

    def __str__(self):
        return self.name

class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions")
    name = models.CharField(max_length=100, verbose_name="Nom de la région")
    code = models.CharField(max_length=20, blank=True, verbose_name="Code régional")

    def __str__(self):
        return f"{self.name} ({self.country})"

class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100, verbose_name="Nom de la ville")

    def __str__(self):
        return f"{self.name} ({self.region})"

@register_snippet
class Tax(models.Model):
    TAX_TYPES = [
        ('standard', 'Standard'),
        ('reduced', 'Réduit'),
        ('exempt', 'Exonéré'),
        ('zero', 'Zéro Rated'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom de la taxe")
    rate = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Taux (%)", validators=[validate_tax_rate]
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="taxes")
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Région")
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Ville")
    tax_type = models.CharField(
        max_length=50, choices=TAX_TYPES, default='standard', verbose_name="Type de taxe"
    )
    site = models.ForeignKey(
    Site, 
    on_delete=models.CASCADE, 
    verbose_name="Site associé",
    null=True, 
    blank=True
    )
    applies_to_foreign = models.BooleanField(default=True, verbose_name="Clients étrangers")
    applies_to_b2b = models.BooleanField(default=True, verbose_name="Clients B2B")
    applies_to_b2c = models.BooleanField(default=True, verbose_name="Clients B2C")
    applies_above_threshold = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name="Seuil minimal (HT)"
    )
    effective_date = models.DateField(
        verbose_name="Date d'entrée en vigueur", validators=[validate_dates]
    )
    end_date = models.DateField(blank=True, null=True, verbose_name="Date de fin")
    version = models.PositiveIntegerField(default=1, verbose_name="Version de la taxe")
    is_active = models.BooleanField(default=True, verbose_name="Taxe active ?")

    class Meta:
        verbose_name = "Taxe"
        verbose_name_plural = "Taxes"
        unique_together = ("name", "rate", "country", "region", "city", "version")
        indexes = [
            models.Index(fields=["country", "region", "city", "site", "effective_date"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.rate}%) - {self.country}"

    def is_active(self):
        from django.utils.timezone import now
        today = now().date()
        return self.effective_date <= today and (not self.end_date or self.end_date >= today)
