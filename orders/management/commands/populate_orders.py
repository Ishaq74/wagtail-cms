from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order, OrderLine
from product.models import ProductPage, ProductVariant
from taxes.models import TaxMatrice
from expeditions.models import ShippingLabel, ShippingOption
from wagtail.models import Page
from random import randint

class Command(BaseCommand):
    help = "Génère des commandes et des lignes de commande factices"

    def handle(self, *args, **kwargs):
        # Création d'une commande fictive
        self.stdout.write("Création des commandes...")

        # Simulation de produits existants pour les lignes de commande
        product = ProductPage.objects.first()
        variant = ProductVariant.objects.first() if ProductVariant.objects.exists() else None
        shipping_option = ShippingOption.objects.first() if ShippingOption.objects.exists() else None
        tax_matrice = TaxMatrice.objects.first()

        # Création d'une commande
        order = Order.objects.create(
            customer_name="Client Test",
            email="test@client.com",
            billing_address="123 Rue Exemple, Paris",
            shipping_address=None,  # À ajuster si nécessaire
            shipping_option=shipping_option,
            total_ht=0.0,
            total_tva=0.0,
            total_ttc=0.0,
            shipping_cost=0.0,
            country="FR",
            status="draft",
            is_invoiced=False,
            is_payed=False,
            created_at=timezone.now(),
        )

        # Ajout de lignes de commande à la commande
        for _ in range(5):  # Ajouter 5 lignes de commande aléatoires
            quantity = randint(1, 5)
            unit_price_ht = round(randint(10, 50), 2)
            unit_price_ttc = unit_price_ht * 1.2  # Prix TTC calculé sur base HT (exemple avec 20% de TVA)
            
            order_line = OrderLine.objects.create(
                order=order,
                product=product,
                variant=variant,
                quantity=quantity,
                unit_price_ht=unit_price_ht,
                unit_price_ttc=unit_price_ttc,
                tax_rate=tax_matrice,
                weight=randint(1, 5),  # Poids aléatoire pour chaque produit
            )

            # Mettre à jour les totaux de la commande après l'ajout des lignes
            order.calculate_totals()

        self.stdout.write(self.style.SUCCESS(f"Commande {order.id} créée avec succès avec {order.lines.count()} lignes de commande."))

