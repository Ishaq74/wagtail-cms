from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_invoice_pdf(invoice):
    """
    Génère un PDF pour une facture spécifique.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.drawString(100, 750, f"Facture: {invoice.number}")
    pdf.drawString(100, 730, f"Client: {invoice.order.customer_name}")
    pdf.drawString(100, 710, f"Total TTC: {invoice.total_ttc} €")
    pdf.save()
    buffer.seek(0)
    return buffer
