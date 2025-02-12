from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.models import Page
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting


@register_setting
class HeaderSettings(BaseGenericSetting):
    """Réglages pour le header avec sélection d’un menu."""
    display_logo = models.BooleanField(default=True, help_text="Afficher le logo dans le Header")
    display_site_title = models.BooleanField(default=True, help_text="Afficher le titre du site dans le Header")
    display_menu = models.BooleanField(default=True, help_text="Afficher le menu de navigation")
    selected_menu = models.ForeignKey(
        'layout.NavigationMenu',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Menu à afficher dans le Header"
    )
    display_account_icon = models.BooleanField(default=True, help_text="Afficher l'icône du compte")
    display_cart_icon = models.BooleanField(default=True, help_text="Afficher l'icône du panier")
    display_cta_button = models.BooleanField(default=False, help_text="Afficher un bouton CTA")
    cta_button_text = models.CharField(max_length=50, blank=True, help_text="Texte du bouton CTA")
    cta_button_url = models.URLField(blank=True, help_text="Lien pour le bouton CTA")
    open_in_new_tab = models.BooleanField(default=False, help_text="Ouvrir le lien du bouton CTA dans un nouvel onglet")

    panels = [
        FieldPanel('display_logo'),
        FieldPanel('display_site_title'),
        FieldPanel('display_menu'),
        FieldPanel('selected_menu'),
        FieldPanel('display_account_icon'),
        FieldPanel('display_cart_icon'),
        FieldPanel('display_cta_button'),
        FieldPanel('cta_button_text'),
        FieldPanel('cta_button_url'),
        FieldPanel('open_in_new_tab'),
    ]


@register_setting
class FooterSettings(BaseGenericSetting):
    """Réglages pour le footer avec sélection de deux menus et gestion des horaires."""
    display_about_section = models.BooleanField(default=True, help_text="Afficher la section 'À propos'")
    display_logo = models.BooleanField(default=True, help_text="Afficher le logo dans le Header")
    display_opening_hours = models.BooleanField(default=True, help_text="Afficher les horaires d'ouverture")
    selected_menu_1 = models.ForeignKey(
        'layout.NavigationMenu',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Premier menu à afficher dans le Footer"
    )
    selected_menu_2 = models.ForeignKey(
        'layout.NavigationMenu',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Second menu à afficher dans le Footer"
    )

    panels = [
        FieldPanel('display_about_section'),
        FieldPanel('display_logo'),
        FieldPanel('display_opening_hours'),
        FieldPanel('selected_menu_1'),
        FieldPanel('selected_menu_2'),
    ]


@register_snippet
class NavigationMenu(ClusterableModel):
    """Modèle principal pour les menus."""
    title = models.CharField(max_length=255, help_text="Nom du menu (ex : MenuHeader, MenuFooter1, etc.)")

    panels = [
        FieldPanel('title'),
        InlinePanel('items', label="Éléments du menu"),
    ]

    def __str__(self):
        return self.title


class NavigationItem(models.Model):
    """Élément d’un menu."""
    menu = ParentalKey(
        NavigationMenu,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Menu auquel cet élément appartient."
    )
    label = models.CharField(max_length=255, help_text="Texte affiché pour le lien.")
    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Page Wagtail à laquelle ce lien pointe."
    )
    custom_url = models.URLField(
        blank=True,
        help_text="Lien personnalisé si aucune page n'est sélectionnée."
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        help_text="Élément parent pour créer des sous-menus."
    )
    sort_order = models.IntegerField(default=0, help_text="Ordre d'affichage.")

    panels = [
        FieldPanel('label'),
        PageChooserPanel('page'),
        FieldPanel('custom_url'),
        FieldPanel('parent'),
        FieldPanel('sort_order'),
    ]

    def get_url(self):
        """Retourne l'URL de l'élément (page ou lien personnalisé)."""
        if self.page:
            return self.page.url
        return self.custom_url

    def __str__(self):
        return self.label
