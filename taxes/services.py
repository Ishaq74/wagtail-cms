from django.db import models
from taxes.models import Tax
from django.utils.timezone import now

class TaxService:
    @staticmethod
    def get_applicable_taxes(product, site, country, region=None, city=None, is_foreign=False, is_b2b=False, amount_ht=0):
        taxes = Tax.objects.filter(city=city) if city else None
        if not taxes or not taxes.exists():
            taxes = Tax.objects.filter(region=region) if region else None
        if not taxes or not taxes.exists():
            taxes = Tax.objects.filter(country=country)

        taxes.filter(
            (models.Q(end_date__isnull=True) | models.Q(end_date__gte=now().date())),
            site=site,
            effective_date__lte=now().date(),
        )

        if is_foreign:
            taxes = taxes.filter(applies_to_foreign=True)
        if is_b2b:
            taxes = taxes.filter(applies_to_b2b=True)
        else:
            taxes = taxes.filter(applies_to_b2c=True)

        return taxes

    @staticmethod
    def calculate_total_taxes(amount_ht, taxes):
        total_tax = sum(amount_ht * (tax.rate / 100) for tax in taxes)
        return round(total_tax, 2)

    @staticmethod
    def calculate_price_with_taxes(amount_ht, product, site, country, region=None, is_foreign=False, is_b2b=False):
        taxes = TaxService.get_applicable_taxes(product, site, country, region, None, is_foreign, is_b2b, amount_ht)
        tax_amount = TaxService.calculate_total_taxes(amount_ht, taxes)
        return {
            "price_ht": amount_ht,
            "tax_amount": tax_amount,
            "price_ttc": round(amount_ht + tax_amount, 2),
            "tax_details": [f"{tax.name} ({tax.rate}%)" for tax in taxes],
        }
