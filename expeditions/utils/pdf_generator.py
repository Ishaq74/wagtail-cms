from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile


def generate_shipping_label_pdf(order_id, shipping_option, weight, dimensions):
    """
    Génère un PDF simple pour le bordereau d'expédition.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    c.drawString(100, 750, f"Bordereau d'expédition - Commande {order_id}")
    c.drawString(100, 730, f"Transporteur : {shipping_option.carrier.name}")
    c.drawString(100, 710, f"Mode : {shipping_option.name}")
    c.drawString(100, 690, f"Poids : {weight} kg")
    c.drawString(100, 670, f"Dimensions : {dimensions}")

    c.save()
    buffer.seek(0)

    return ContentFile(buffer.read(), name=f"label_{order_id}.pdf")
