import requests

class VATValidationService:
    @staticmethod
    def validate_vat_number(vat_number, country_code):
        url = f"https://ec.europa.eu/taxation_customs/vies/vatResponse.html?vat={vat_number}&country={country_code}"
        response = requests.get(url)
        if response.status_code == 200 and "Valid VAT number" in response.text:
            return True
        return False
