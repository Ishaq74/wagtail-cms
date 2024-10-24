from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

# Sous-modèle pour les horaires
class Horaire(models.Model):
    jour = models.CharField(max_length=20, help_text="Jour de la semaine", choices=[
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    ])
    heure_debut = models.TimeField(blank=True, null=True, help_text="Heure d'ouverture (laisser vide si fermé).")
    heure_fin = models.TimeField(blank=True, null=True, help_text="Heure de fermeture (laisser vide si fermé).")
    parent = ParentalKey('HorairesOuverture', related_name='horaires')

    panels = [
        FieldPanel('jour'),
        FieldPanel('heure_debut'),
        FieldPanel('heure_fin'),
    ]

    class Meta:
        verbose_name = "Horaire"
        verbose_name_plural = "Horaires"


# Modèle principal pour les horaires d'ouverture
@register_setting
class HorairesOuverture(ClusterableModel, BaseGenericSetting):
    panels = [
        MultiFieldPanel([
            InlinePanel('horaires', label="Horaires d'ouverture par jour"),
        ], heading="Horaires d'ouverture")
    ]


# Modèle pour l'organisation (Identité légale)
@register_setting
class OrganisationSettings(BaseGenericSetting):
    nom_entreprise = models.CharField(max_length=255, help_text="Nom de l'entreprise")
    numero_siret = models.CharField(max_length=14, help_text="Numéro de SIRET")
    numero_tva = models.CharField(max_length=50, blank=True, help_text="Numéro de TVA")
    capital_social = models.CharField(max_length=50, blank=True, help_text="Capital social de l'entreprise")
    forme_juridique = models.CharField(max_length=50, blank=True, help_text="Forme juridique (SARL, SAS, etc.)")

    adresse_rue = models.CharField(max_length=255, help_text="Rue de l'adresse du siège social")
    adresse_code_postal = models.CharField(max_length=10, help_text="Code postal")
    adresse_ville = models.CharField(max_length=100, help_text="Ville")
    adresse_pays = models.CharField(max_length=100, help_text="Pays")

    panels = [
        MultiFieldPanel([
            FieldPanel('nom_entreprise'),
            FieldPanel('numero_siret'),
            FieldPanel('numero_tva'),
            FieldPanel('capital_social'),
            FieldPanel('forme_juridique'),
        ], heading="Fiche d'identité de l'entreprise"),
        MultiFieldPanel([
            FieldPanel('adresse_rue'),
            FieldPanel('adresse_code_postal'),
            FieldPanel('adresse_ville'),
            FieldPanel('adresse_pays'),
        ], heading="Adresse du siège social"),
    ]


# Modèle pour le contact de l'entreprise
@register_setting
class ContactSettings(BaseGenericSetting):
    nom_contact = models.CharField(max_length=255, help_text="Nom du contact principal")
    telephone = models.CharField(max_length=20, help_text="Numéro de téléphone")
    email = models.EmailField(help_text="Adresse email")

    adresse_rue_contact = models.CharField(max_length=255, help_text="Rue de l'adresse de contact")
    adresse_code_postal_contact = models.CharField(max_length=10, help_text="Code postal de l'adresse de contact")
    adresse_ville_contact = models.CharField(max_length=100, help_text="Ville de l'adresse de contact")
    adresse_pays_contact = models.CharField(max_length=100, help_text="Pays de l'adresse de contact")

    panels = [
        MultiFieldPanel([
            FieldPanel('nom_contact'),
            FieldPanel('telephone'),
            FieldPanel('email'),
        ], heading="Informations de contact"),
        MultiFieldPanel([
            FieldPanel('adresse_rue_contact'),
            FieldPanel('adresse_code_postal_contact'),
            FieldPanel('adresse_ville_contact'),
            FieldPanel('adresse_pays_contact'),
        ], heading="Adresse de contact"),
    ]


# Modèle pour les réseaux sociaux
@register_setting
class SocialMediaSettings(BaseGenericSetting):
    instagram_url = models.URLField(blank=True, help_text="URL du profil Instagram")
    tiktok_url = models.URLField(blank=True, help_text="URL du profil TikTok")
    linkedin_url = models.URLField(blank=True, help_text="URL du profil LinkedIn")

    panels = [
        MultiFieldPanel([
            FieldPanel('instagram_url'),
            FieldPanel('tiktok_url'),
            FieldPanel('linkedin_url'),
        ], heading="Réseaux sociaux")
    ]


# Modèle pour les mentions légales
@register_setting
class MentionsLegalesSettings(BaseGenericSetting):
    hebergeur_nom = models.CharField(max_length=255, help_text="Nom de l'hébergeur")
    hebergeur_adresse_rue = models.CharField(max_length=255, help_text="Rue de l'adresse de l'hébergeur")
    hebergeur_adresse_code_postal = models.CharField(max_length=10, help_text="Code postal de l'hébergeur")
    hebergeur_adresse_ville = models.CharField(max_length=100, help_text="Ville de l'hébergeur")
    hebergeur_adresse_pays = models.CharField(max_length=100, help_text="Pays de l'hébergeur")
    hebergeur_contact = models.CharField(max_length=50, help_text="Contact de l'hébergeur")

    responsable_publication = models.CharField(max_length=255, help_text="Nom du responsable de la publication")
    proprietaire_site = models.CharField(max_length=255, help_text="Nom du propriétaire du site")
    cgu_url = models.URLField(blank=True, help_text="URL vers les conditions générales d'utilisation")

    panels = [
        MultiFieldPanel([
            FieldPanel('hebergeur_nom'),
            FieldPanel('hebergeur_adresse_rue'),
            FieldPanel('hebergeur_adresse_code_postal'),
            FieldPanel('hebergeur_adresse_ville'),
            FieldPanel('hebergeur_adresse_pays'),
            FieldPanel('hebergeur_contact'),
        ], heading="Informations de l'hébergeur"),
        MultiFieldPanel([
            FieldPanel('responsable_publication'),
            FieldPanel('proprietaire_site'),
            FieldPanel('cgu_url'),
        ], heading="Informations légales"),
    ]


# Modèle pour les partenaires
@register_setting
class PartenairesSettings(ClusterableModel, BaseGenericSetting):
    class Partenaire(models.Model):
        partenaire_nom = models.CharField(max_length=255, help_text="Nom du partenaire")
        partenaire_logo = models.ForeignKey(
            'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
            help_text="Logo du partenaire"
        )
        partenaire_url = models.URLField(help_text="Lien vers le site du partenaire")
        partenaire_alt = models.CharField(max_length=255, help_text="Texte alternatif pour le logo du partenaire")
        parent = ParentalKey('PartenairesSettings', related_name='partenaires')

        panels = [
            FieldPanel('partenaire_nom'),
            FieldPanel('partenaire_logo'),
            FieldPanel('partenaire_alt'),
            FieldPanel('partenaire_url'),
        ]

    panels = [
        MultiFieldPanel([
            InlinePanel('partenaires', label="Partenaires"),
        ], heading="Partenaires"),
    ]


# Modèle pour le logo et favicon
@register_setting
class MediaSettings(BaseGenericSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
        help_text="Logo de l'entreprise"
    )
    favicon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
        help_text="Favicon du site"
    )
    logo_alt = models.CharField(max_length=255, help_text="Texte alternatif pour le logo")
    favicon_alt = models.CharField(max_length=255, help_text="Texte alternatif pour le favicon")

    panels = [
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('logo_alt'),
        ], heading="Logo"),
        MultiFieldPanel([
            FieldPanel('favicon'),
            FieldPanel('favicon_alt'),
        ], heading="Favicon"),
    ]
