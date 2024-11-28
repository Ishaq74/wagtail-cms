from django.test import TestCase
from taxes.models import Tax
from product.models import ProductPage

class TaxServiceTest(TestCase):
    def setUp(self):
        self.tax = Tax.objects.create(
            name="TVA",
            rate=20.0,
            country="FR",
            applies_to_foreign=True,
            applies_to_b2b=True,
            applies_to_b2c=True,
            tax_type="standard",
            effective_date="2024-01-01",
        )

        self.product = ProductPage.objects.create(
            title="Produit Test",
            price=100.0,
        )

    def test_simulation(self):
        from taxes.services import TaxService

        simulation = TaxService.simulate_tax_configuration(
            product=self.product,
            country="FR",
            is_foreign=False,
            is_b2b=False,
            amount_ht=100.0,
        )

        self.assertEqual(simulation["price_ttc"], 120.0)
