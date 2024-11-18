from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index
from taggit.models import Tag, TaggedItemBase
from modelcluster.fields import ParentalKey
from wagtail import blocks
from modelcluster.tags import ClusterTaggableManager
from streams import blocks as custom_blocks

# Modèle pour les tags
class BusinessLocalTag(TaggedItemBase):
    content_object = ParentalKey('BusinessLocalPage', related_name='tagged_items', on_delete=models.CASCADE)

# Page d'accueil de l'annuaire des entreprises locales
class BusinessLocalIndexPage(Page):
    max_count = 1
    excerpt = models.TextField(max_length=250, blank=True, help_text='Texte affiché en haut de la page')
    content = RichTextField(blank=True)
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Image principale de la page")
    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
        ('paginated_product_list', custom_blocks.PaginatedProductListBlock()),
        ('limited_product_list', custom_blocks.LimitedProductListBlock()),
        ('paginated_product_category_list', custom_blocks.PaginatedProductCategoryListBlock()),
        ('limited_product_category_list', custom_blocks.LimitedProductCategoryListBlock()),
        ('paginated_blog_list', custom_blocks.PaginatedBlogListBlock()),
        ('limited_blog_list', custom_blocks.LimitedBlogListBlock()),
        ('paginated_blog_category_list', custom_blocks.PaginatedBlogCategoryListBlock()),
        ('limited_blog_category_list', custom_blocks.LimitedBlogCategoryListBlock()),
        ('paginated_service_list', custom_blocks.PaginatedServiceListBlock()),
        ('limited_service_list', custom_blocks.LimitedServiceListBlock()),
        ('paginated_service_category_list', custom_blocks.PaginatedServiceCategoryListBlock()),
        ('limited_service_category_list', custom_blocks.LimitedServiceCategoryListBlock()),
        ('paginated_businesslocal_list', custom_blocks.PaginatedBusinessLocalListBlock()),
        ('limited_businesslocal_list', custom_blocks.LimitedBusinessLocalListBlock()),
        ('paginated_businesslocal_category_list', custom_blocks.PaginatedBusinessLocalCategoryListBlock()),
        ('limited_businesslocal_category_list', custom_blocks.LimitedBusinessLocalCategoryListBlock()),
    ], null=True, blank=True, use_json_field=True)


    content_panels = Page.content_panels + [
        FieldPanel('excerpt'),
        FieldPanel('content'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]

    subpage_types = ['BusinessLocalCategory']

    def get_context(self, request):
        context = super().get_context(request)
        featured_only = request.GET.get('featured', False)
        categories = self.get_children().live().type(BusinessLocalCategory)
        if featured_only:
            categories = categories.filter(specific__is_featured=True)
        
        search_query = request.GET.get('query', None)
        if search_query:
            categories = categories.search(search_query, fields=["title", "summary"])

        paginator = Paginator(categories, 3)
        page = request.GET.get('page')
        try:
            categories_paginated = paginator.page(page)
        except PageNotAnInteger:
            categories_paginated = paginator.page(1)
        except EmptyPage:
            categories_paginated = paginator.page(paginator.num_pages)

        featured_businesses = BusinessLocalPage.objects.live().filter(is_featured=True)[:3]
        context.update({
            'categories': categories_paginated,
            'search_query': search_query,
            'pagination': categories_paginated,
            'featured_businesses': featured_businesses,
        })
        return context

    page_description = "Page d'accueil de l'Annuaire des Organisations"

    class Meta:
        verbose_name = "Annuaire"
        verbose_name_plural = "Annuaire"
        
# Page de catégorie pour les entreprises locales
class BusinessLocalCategory(Page):
    excerpt = models.CharField(max_length=250, blank=True, help_text="Résumé de la catégorie")
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    is_featured = models.BooleanField(default=False, help_text="Mettre cette catégorie en avant")
    content = RichTextField(blank=True)

    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
        ('paginated_product_list', custom_blocks.PaginatedProductListBlock()),
        ('limited_product_list', custom_blocks.LimitedProductListBlock()),
        ('paginated_product_category_list', custom_blocks.PaginatedProductCategoryListBlock()),
        ('limited_product_category_list', custom_blocks.LimitedProductCategoryListBlock()),
        ('paginated_blog_list', custom_blocks.PaginatedBlogListBlock()),
        ('limited_blog_list', custom_blocks.LimitedBlogListBlock()),
        ('paginated_blog_category_list', custom_blocks.PaginatedBlogCategoryListBlock()),
        ('limited_blog_category_list', custom_blocks.LimitedBlogCategoryListBlock()),
        ('paginated_service_list', custom_blocks.PaginatedServiceListBlock()),
        ('limited_service_list', custom_blocks.LimitedServiceListBlock()),
        ('paginated_service_category_list', custom_blocks.PaginatedServiceCategoryListBlock()),
        ('limited_service_category_list', custom_blocks.LimitedServiceCategoryListBlock()),
        ('paginated_businesslocal_list', custom_blocks.PaginatedBusinessLocalListBlock()),
        ('limited_businesslocal_list', custom_blocks.LimitedBusinessLocalListBlock()),
        ('paginated_businesslocal_category_list', custom_blocks.PaginatedBusinessLocalCategoryListBlock()),
        ('limited_businesslocal_category_list', custom_blocks.LimitedBusinessLocalCategoryListBlock()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('excerpt'),
        FieldPanel('featured_image'),
        FieldPanel('is_featured'),
        FieldPanel('content'),
        FieldPanel('body'),
    ]

    parent_page_types = ['BusinessLocalIndexPage']
    subpage_types = ['BusinessLocalPage', 'BusinessLocalCategory']

    def get_context(self, request):
        context = super().get_context(request)
        featured_only = request.GET.get('featured', False)
        businesses = self.get_children().live().type(BusinessLocalPage)
        if featured_only:
            businesses = businesses.filter(specific__is_featured=True)

        paginator = Paginator(businesses, 5)
        page = request.GET.get('page')
        try:
            businesses_paginated = paginator.page(page)
        except PageNotAnInteger:
            businesses_paginated = paginator.page(1)
        except EmptyPage:
            businesses_paginated = paginator.page(paginator.num_pages)

        context.update({
            'businesses': businesses_paginated,
            'pagination': businesses_paginated,
        })
        return context

    page_description = "Page de catégorie pour les entreprises locales"

    class Meta:
        verbose_name = "Page de Catégorie"
        verbose_name_plural = "Pages de Catégorie"

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
        verbose_name = "Horaires d'ouverture"

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
    content = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    google_maps_link = models.URLField(blank=True, help_text="Lien Google Maps", editable=True)
    tags = ClusterTaggableManager(through=BusinessLocalTag, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Mettre cette entreprise en avant")
    opening_hours = StreamField([
        ('hours', OpeningHoursBlock())
    ], blank=True, help_text="Horaires d'ouverture flexibles")
    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
        ('paginated_product_list', custom_blocks.PaginatedProductListBlock()),
        ('limited_product_list', custom_blocks.LimitedProductListBlock()),
        ('paginated_product_category_list', custom_blocks.PaginatedProductCategoryListBlock()),
        ('limited_product_category_list', custom_blocks.LimitedProductCategoryListBlock()),
        ('paginated_blog_list', custom_blocks.PaginatedBlogListBlock()),
        ('limited_blog_list', custom_blocks.LimitedBlogListBlock()),
        ('paginated_blog_category_list', custom_blocks.PaginatedBlogCategoryListBlock()),
        ('limited_blog_category_list', custom_blocks.LimitedBlogCategoryListBlock()),
        ('paginated_service_list', custom_blocks.PaginatedServiceListBlock()),
        ('limited_service_list', custom_blocks.LimitedServiceListBlock()),
        ('paginated_service_category_list', custom_blocks.PaginatedServiceCategoryListBlock()),
        ('limited_service_category_list', custom_blocks.LimitedServiceCategoryListBlock()),
        ('paginated_businesslocal_list', custom_blocks.PaginatedBusinessLocalListBlock()),
        ('limited_businesslocal_list', custom_blocks.LimitedBusinessLocalListBlock()),
        ('paginated_businesslocal_category_list', custom_blocks.PaginatedBusinessLocalCategoryListBlock()),
        ('limited_businesslocal_category_list', custom_blocks.LimitedBusinessLocalCategoryListBlock()),
    ], null=True, blank=True, use_json_field=True)

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
        FieldPanel('content'),
        FieldPanel('featured_image'),
        InlinePanel('gallery_images', label="Galerie d'images"),
        FieldPanel('tags'),
        FieldPanel('opening_hours'),
        FieldPanel('google_maps_link'),
        FieldPanel('body'),
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

    page_description = "Page d'entreprise pour une entreprise locale"

    class Meta:
        verbose_name = "Page d'entreprise"
        verbose_name_plural = "Pages d'entreprises"
