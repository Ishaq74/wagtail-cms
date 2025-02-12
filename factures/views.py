from django.shortcuts import render, get_object_or_404
from .models import Invoice


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, "factures/invoice_detail.html", {"invoice": invoice})


def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "factures/invoice_list.html", {"invoices": invoices})
