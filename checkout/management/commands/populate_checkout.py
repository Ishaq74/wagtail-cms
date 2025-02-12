from django.core.management.base import BaseCommand
from django.conf import settings
from checkout.models import CheckoutSettings, Order
from decimal import Decimal
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Populate the 'checkout' app with initial settings and example orders"

    def handle(self, *args, **kwargs):
        self.populate_checkout_settings()
        self.populate_orders()

    def populate_checkout_settings(self):
        """Populate CheckoutSettings with default values."""
        settings, created = CheckoutSettings.objects.get_or_create(
            id=1,  # Assuming only one instance of CheckoutSettings
            defaults={
                "store_name": "Casa Nela",
                "currency": "EUR",
                "tax_rate_default": Decimal("20.00"),
                "enable_delivery": True,
                "enable_pickup": True,
                "enable_stripe": True,
                "enable_cod": True,
                "stripe_api_key": "sk_test_4eC39HqLyjWDarjtT1zdp7dc",
                "stripe_publishable_key": "pk_test_TYooMQauvdEDq54NiTphI7jx",
                "enable_email_notifications": True,
                "email_subject": "Confirmation de commande",
                "email_body_template": "Merci pour votre commande #{order_id}. Total : {total} {currency}.",
                "email_host": "smtp.example.com",
                "email_port": 587,
                "email_host_user": "user@example.com",
                "email_host_password": "securepassword",
                "opening_hours": {
                    "Monday": {"open": "09:00", "close": "18:00"},
                    "Tuesday": {"open": "09:00", "close": "18:00"},
                    "Wednesday": {"open": "09:00", "close": "18:00"},
                    "Thursday": {"open": "09:00", "close": "18:00"},
                    "Friday": {"open": "09:00", "close": "18:00"},
                    "Saturday": {"open": "10:00", "close": "16:00"},
                    "Sunday": {"open": None, "close": None},
                },
            }
        )

        if created:
            self.stdout.write("Checkout settings created successfully.")
        else:
            self.stdout.write("Checkout settings already exist.")

    def populate_orders(self):
        """Populate the Order model with example data."""
        # Récupérer le modèle utilisateur configuré
        CustomUser = get_user_model()
        user = CustomUser.objects.filter(username="admin").first()
        if not user:
            self.stdout.write("Admin user not found. Create an admin user first.")
            return

        orders = [
            {
                "user": user,
                "total_amount": Decimal("59.99"),
                "payment_method": "Stripe",
                "delivery_option": "delivery",
                "delivery_address": "123 Rue de Test, Paris",
                "phone_number": "0123456789",
                "email": "client@example.com",
                "status": "ordered",
            },
            {
                "user": user,
                "total_amount": Decimal("29.99"),
                "payment_method": "COD",
                "delivery_option": "pickup",
                "delivery_address": None,
                "phone_number": "0123456789",
                "email": "pickupclient@example.com",
                "status": "ready",
            },
        ]

        for order_data in orders:
            order, created = Order.objects.get_or_create(
                user=order_data["user"],
                total_amount=order_data["total_amount"],
                payment_method=order_data["payment_method"],
                delivery_option=order_data["delivery_option"],
                defaults=order_data,
            )
            if created:
                self.stdout.write(f"Order created: {order}")
            else:
                self.stdout.write(f"Order already exists: {order}")
