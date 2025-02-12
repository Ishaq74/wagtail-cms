from django.core.management.base import BaseCommand
from factures.models import Invoice
from orders.models import Order

class Command(BaseCommand):
    help = "Generate invoices from confirmed orders"

    def handle(self, *args, **kwargs):
        confirmed_orders = Order.objects.filter(status="confirmed", is_invoiced=False)

        if not confirmed_orders.exists():
            self.stdout.write("No confirmed orders available for invoicing.")
            return

        for order in confirmed_orders:
            try:
                order.convert_to_invoice()
                self.stdout.write(self.style.SUCCESS(f"Invoice generated for order {order.id}."))
            except Exception as e:
                self.stderr.write(f"Error generating invoice for order {order.id}: {e}")
