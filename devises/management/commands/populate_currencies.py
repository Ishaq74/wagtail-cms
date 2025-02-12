from django.core.management.base import BaseCommand
from devises.models import Currency


class Command(BaseCommand):
    help = "Ajoute des devises de base avec leurs taux par rapport à l'Euro"

    def handle(self, *args, **kwargs):
        currencies = [
            {"code": "EUR",},
            {"code": "USD",},
            {"code": "GBP",},
            {"code": "JPY",},
        ]

        for currency_data in currencies:
            Currency.objects.update_or_create(
                code=currency_data["code"],
                defaults={"rate_to_euro": currency_data["rate_to_euro"]},
            )
        self.stdout.write(self.style.SUCCESS("Devises ajoutées avec succès."))
