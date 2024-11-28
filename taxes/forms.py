from django import forms
from wagtail.admin.panels import HelpPanel

class TaxAdminForm(forms.ModelForm):
    panels = [
        HelpPanel(content="Utilisez ce champ pour configurer des taxes spécifiques à une région ou une ville."),
        HelpPanel(content="Assurez-vous que les taux ne se chevauchent pas entre les différentes juridictions."),
    ]
