import requests


def track_shipment(carrier, tracking_number):
    """
    Effectue une requête de suivi auprès de l'API du transporteur.
    """
    if not carrier.api_url:
        raise ValueError(f"L'API du transporteur {carrier.name} n'est pas configurée.")

    response = requests.get(f"{carrier.api_url}/track/{tracking_number}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Erreur lors du suivi du colis : {response.text}")
