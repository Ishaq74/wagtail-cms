from .models import ShippingLabel
from .utils.pdf_generator import generate_shipping_label_pdf


def create_shipping_label(order_id, shipping_option, weight, dimensions):
    """
    Crée un bordereau d'expédition.
    """
    if weight > shipping_option.max_weight:
        raise ValueError("Le poids excède la limite autorisée pour cette option.")

    # Générer le PDF du bordereau
    pdf_path = generate_shipping_label_pdf(order_id, shipping_option, weight, dimensions)

    # Enregistrer le bordereau en base
    label = ShippingLabel.objects.create(
        shipping_option=shipping_option,
        order_id=order_id,
        pdf_label=pdf_path,
    )
    return label
