from django.core.management.base import BaseCommand
from expeditions.models import ShippingOption, Carrier


class Command(BaseCommand):
    help = "Ajoute des options d'expédition de base"

    def handle(self, *args, **kwargs):
        # Créez ou récupérez un transporteur par défaut
        default_carrier, _ = Carrier.objects.get_or_create(
            name="Transporteur par défaut",
            defaults={
                "api_url": "https://default-carrier.example.com",
                "is_active": True,
            },
        )

        shipping_options = [
            {"name": "Standard", "base_price": 5.0, "per_kg_price": 0.5, "max_weight": 30.0, "delivery_type": "standard"},
            {"name": "Express", "base_price": 10.0, "per_kg_price": 1.0, "max_weight": 20.0, "delivery_type": "express"},
            {"name": "Retrait en magasin", "base_price": 0.0, "per_kg_price": 0.0, "max_weight": 50.0, "delivery_type": "pickup"},
        ]

        for option_data in shipping_options:
            ShippingOption.objects.update_or_create(
                name=option_data["name"],
                defaults={
                    "carrier": default_carrier,
                    "base_price": option_data["base_price"],
                    "per_kg_price": option_data["per_kg_price"],
                    "max_weight": option_data["max_weight"],
                    "delivery_type": option_data["delivery_type"],
                },
            )
        self.stdout.write(self.style.SUCCESS("Options d'expédition ajoutées avec succès."))