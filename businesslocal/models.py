from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.images.models import Image
from wagtail.search import index
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from taggit.models import Tag, TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager


# Modèle pour les tags
class BusinessLocalTag(TaggedItemBase):
    content_object = ParentalKey('BusinessLocalPage', related_name='tagged_items', on_delete=models.CASCADE)


# Page d'accueil de l'annuaire des entreprises locales
class BusinessLocalIndexPage(Page):
    max_count = 1
    subtitle = models.CharField(max_length=255, default="Annuaire d'entreprises locales")
    summary = models.TextField(max_length=250, blank=True, help_text='Texte affiché en haut de la page')
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('summary'),
        FieldPanel('body'),
    ]

    subpage_types = ['BusinessLocalCategory']

    def get_context(self, request):
        context = super().get_context(request)

        # Filtrer les catégories (option pour n'afficher que les catégories "featured")
        featured_only = request.GET.get('featured', False)
        if featured_only:
            categories = self.get_children().live().type(BusinessLocalCategory).filter(specific__is_featured=True)
        else:
            categories = self.get_children().live().type(BusinessLocalCategory)

        # Recherche
        search_query = request.GET.get('query', None)
        if search_query:
            categories = categories.search(search_query, fields=["title", "summary"])

        # Pagination
        paginator = Paginator(categories, 3)
        page = request.GET.get('page')

        try:
            categories_paginated = paginator.page(page)
        except PageNotAnInteger:
            categories_paginated = paginator.page(1)
        except EmptyPage:
            categories_paginated = paginator.page(paginator.num_pages)

        # Récupérer les entreprises "mis en avant"
        featured_businesses = BusinessLocalPage.objects.live().filter(is_featured=True)[:3]

        context['categories'] = categories_paginated
        context['search_query'] = search_query
        context['pagination'] = categories_paginated  # Pagination dans le template
        context['featured_businesses'] = featured_businesses  # Ajouter les entreprises mises en avant
        return context


# Page de catégorie pour les entreprises locales
class BusinessLocalCategory(Page):
    summary = models.CharField(max_length=250, blank=True, help_text="Résumé de la catégorie")
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    is_featured = models.BooleanField(default=False, help_text="Mettre cette catégorie en avant")

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('featured_image'),  # Utilisation de FieldPanel pour l'image
        FieldPanel('is_featured'),
    ]

    parent_page_types = ['BusinessLocalIndexPage']
    subpage_types = ['BusinessLocalPage', 'BusinessLocalCategory']

    def get_context(self, request):
        context = super().get_context(request)

        # Filtrer les entreprises (option pour n'afficher que les entreprises "featured")
        featured_only = request.GET.get('featured', False)
        businesses = self.get_children().live().type(BusinessLocalPage)
        if featured_only:
            businesses = businesses.filter(specific__is_featured=True)

        # Pagination pour les entreprises
        paginator = Paginator(businesses, 5)
        page = request.GET.get('page')

        try:
            businesses_paginated = paginator.page(page)
        except PageNotAnInteger:
            businesses_paginated = paginator.page(1)
        except EmptyPage:
            businesses_paginated = paginator.page(paginator.num_pages)

        context['businesses'] = businesses_paginated
        context['pagination'] = businesses_paginated  # Pagination pour les entreprises
        return context


# Bloc Struct pour les horaires d'ouverture flexibles
class OpeningHoursBlock(blocks.StructBlock):
    day = blocks.ChoiceBlock(choices=[
        ('monday', 'Lundi'),
        ('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),
        ('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),
        ('saturday', 'Samedi'),
        ('sunday', 'Dimanche'),
    ], label="Jour")
    open_time = blocks.TimeBlock(required=False, label="Heure d'ouverture", help_text="Format HH:MM")
    close_time = blocks.TimeBlock(required=False, label="Heure de fermeture", help_text="Format HH:MM")
    second_open_time = blocks.TimeBlock(required=False, label="Deuxième créneau d'ouverture", help_text="Format HH:MM (facultatif)")
    second_close_time = blocks.TimeBlock(required=False, label="Deuxième créneau de fermeture", help_text="Format HH:MM (facultatif)")
    closed = blocks.BooleanBlock(required=False, label="Fermé toute la journée", help_text="Cocher si l'entreprise est fermée toute la journée")

    class Meta:
        template = 'blocks/opening_hours.html'


# Modèle pour les images de la galerie
class BusinessLocalGalleryImage(models.Model):
    page = ParentalKey('BusinessLocalPage', on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


# Page pour une entreprise locale
class BusinessLocalPage(Page):
    address = models.CharField(max_length=250, help_text="Adresse de l'entreprise")
    phone_number = models.CharField(max_length=20, blank=True, help_text="Numéro de téléphone")
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    body = RichTextField(blank=True, help_text="Description complète de l'entreprise")
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    google_maps_link = models.URLField(blank=True, help_text="Lien Google Maps", editable=True)
    tags = ClusterTaggableManager(through=BusinessLocalTag, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Mettre cette entreprise en avant")
    opening_hours = StreamField([
        ('hours', OpeningHoursBlock())
    ], blank=True, help_text="Horaires d'ouverture flexibles")

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('address'),
        index.FilterField('tags'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('title'),
        FieldPanel('is_featured'),
        FieldPanel('address'),
        FieldPanel('phone_number'),
        FieldPanel('email'),
        FieldPanel('website'),
        FieldPanel('body'),
        FieldPanel('featured_image'),
        InlinePanel('gallery_images', label="Galerie d'images"),  # InlinePanel pour la galerie
        FieldPanel('tags'),
        FieldPanel('opening_hours'),
    ]

    parent_page_types = ['BusinessLocalCategory']
    subpage_types = []

    def get_siblings(self):
        siblings = BusinessLocalPage.objects.live().sibling_of(self).exclude(id=self.id)[:3]
        return siblings

    def get_context(self, request):
        context = super().get_context(request)
        context['related_businesses'] = self.get_siblings()
        return context
