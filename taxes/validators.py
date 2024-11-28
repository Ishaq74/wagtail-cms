from django.core.exceptions import ValidationError
from django.utils.timezone import now

def validate_tax_rate(value):
    if value < 0 or value > 100:
        raise ValidationError("Le taux doit être compris entre 0% et 100%.")

def validate_dates(value):
    if value > now().date():
        raise ValidationError("La date d'entrée en vigueur ne peut pas être dans le futur.")
