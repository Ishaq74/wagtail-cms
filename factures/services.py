from django.core.mail import EmailMessage
from django.conf import settings


def send_invoice_email(invoice, recipient_email):
    """
    Envoie une facture par email.
    """
    subject = f"Votre facture {invoice.number}"
    body = f"Veuillez trouver ci-joint votre facture {invoice.number}."
    pdf = invoice.generate_pdf()

    email = EmailMessage(
        subject, body, settings.DEFAULT_FROM_EMAIL, [recipient_email]
    )
    email.attach(f"facture_{invoice.number}.pdf", pdf.read(), "application/pdf")
    email.send()
