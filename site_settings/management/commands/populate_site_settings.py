from django.core.management.base import BaseCommand
from site_settings.models import (
    HorairesOuverture,
    OrganisationSettings,
    ContactSettings,
    SocialMediaSettings,
    MentionsLegalesSettings,
    PartenairesSettings,
    MediaSettings,
)
from wagtail.images.models import Image


class Command(BaseCommand):
    help = "Populate the site settings with default values for Casa Nela"

    def handle(self, *args, **kwargs):
        self.populate_settings()

    def populate_settings(self):
        self.populate_horaires()
        self.populate_organisation()
        self.populate_contact()
        self.populate_social_media()
        self.populate_mentions_legales()
        self.populate_partenaires()
        self.populate_media()
        self.stdout.write("Les paramètres du site ont été peuplés avec succès.")

    def populate_horaires(self):
        horaires, created = HorairesOuverture.objects.get_or_create()
        if not created:
            self.stdout.write("Les horaires d'ouverture existent déjà.")
            return

        horaires.horaires.create(jour="Lundi", heure_debut="08:00", heure_fin="18:00")
        horaires.horaires.create(jour="Mardi", heure_debut="08:00", heure_fin="18:00")
        horaires.horaires.create(jour="Mercredi", heure_debut="08:00", heure_fin="18:00")
        horaires.horaires.create(jour="Jeudi", heure_debut="08:00", heure_fin="18:00")
        horaires.horaires.create(jour="Vendredi", heure_debut="08:00", heure_fin="18:00")
        horaires.horaires.create(jour="Samedi", heure_debut="09:00", heure_fin="13:00")
        self.stdout.write("Horaires d'ouverture peuplés.")

    def populate_organisation(self):
        organisation, created = OrganisationSettings.objects.get_or_create()
        if not created:
            self.stdout.write("Les informations d'organisation existent déjà.")
            return

        organisation.nom_entreprise = "Casa Nela"
        organisation.numero_siret = "12345678901234"
        organisation.numero_tva = "FR12345678901"
        organisation.capital_social = "50 000 EUR"
        organisation.forme_juridique = "SARL"
        organisation.adresse_rue = "1 Rue de la Paix"
        organisation.adresse_code_postal = "74000"
        organisation.adresse_ville = "Annecy"
        organisation.adresse_pays = "France"
        organisation.save()
        self.stdout.write("Informations d'organisation peuplées.")

    def populate_contact(self):
        contact, created = ContactSettings.objects.get_or_create()
        if not created:
            self.stdout.write("Les informations de contact existent déjà.")
            return

        contact.nom_contact = "Service Client Casa Nela"
        contact.telephone = "+33 4 50 00 00 00"
        contact.email = "contact@casanela.com"
        contact.adresse_rue_contact = "1 Rue de la Paix"
        contact.adresse_code_postal_contact = "74000"
        contact.adresse_ville_contact = "Annecy"
        contact.adresse_pays_contact = "France"
        contact.save()
        self.stdout.write("Informations de contact peuplées.")

    def populate_social_media(self):
        social, created = SocialMediaSettings.objects.get_or_create()
        if not created:
            self.stdout.write("Les informations des réseaux sociaux existent déjà.")
            return

        social.facebook_url = "https://www.facebook.com/casanela"
        social.instagram_url = "https://www.instagram.com/casanela"
        social.linkedin_url = "https://www.linkedin.com/company/casanela"
        social.save()
        self.stdout.write("Réseaux sociaux peuplés.")

    def populate_mentions_legales(self):
        mentions, created = MentionsLegalesSettings.objects.get_or_create()
        if not created:
            self.stdout.write("Les mentions légales existent déjà.")
            return

        mentions.hebergeur_nom = "OVH"
        mentions.responsable_publication = "Marie Dupont"
        mentions.proprietaire_site = "Casa Nela"
        mentions.save()
        self.stdout.write("Mentions légales peuplées.")

    def populate_partenaires(self):
        partenaires, created = PartenairesSettings.objects.get_or_create()
        if not created:
            self.stdout.write("Les partenaires existent déjà.")
            return

        partenaire_logo = Image.objects.filter(title="Logo Partenaire").first()  # Assurez-vous que l'image existe
        partenaires.partenaires.create(
            partenaire_nom="Partenaire A",
            partenaire_logo=partenaire_logo,
            partenaire_url="https://www.partenaire-a.com",
        )
        partenaires.partenaires.create(
            partenaire_nom="Partenaire B",
            partenaire_logo=partenaire_logo,
            partenaire_url="https://www.partenaire-b.com",
        )
        self.stdout.write("Partenaires peuplés.")

    def populate_media(self):
        media, created = MediaSettings.objects.get_or_create()
        if not created:
            self.stdout.write("Les médias (logo et favicon) existent déjà.")
            return

        media.logo = Image.objects.filter(title="Logo Principal").first()  # Assurez-vous que l'image existe
        media.favicon = Image.objects.filter(title="Favicon").first()  # Assurez-vous que l'image existe
        media.logo_alt = "Logo Casa Nela"
        media.favicon_alt = "Favicon Casa Nela"
        media.save()
        self.stdout.write("Médias peuplés.")
