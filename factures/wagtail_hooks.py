from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.models import register_snippet
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Invoice


class InvoiceViewSet(SnippetViewSet):
    model = Invoice
    menu_label = "Factures"
    menu_icon = "doc-full"
    list_display = ("number", "order", "total_ttc", "created_at", "status", "cancelled_at")
    search_fields = ("number", "order__customer_name")

    def cancel_invoice_action(self, request, invoice_id):
        invoice = Invoice.objects.get(id=invoice_id)
        reason = request.GET.get("reason", "Non spécifiée")
        invoice.cancel_invoice(reason)
        messages.success(request, f"Facture {invoice.number} annulée avec succès.")
        return redirect("wagtailadmin_explore", args=[self.get_explore_parent_id()])


register_snippet(InvoiceViewSet)
