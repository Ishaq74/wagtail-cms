from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .blocks import PaginatedServiceListBlock, LimitedServiceListBlock, SiblingsServiceListBlock
from streams import blocks as custom_blocks  # Assure-toi que ce chemin est correct

class ServicePage(Page):
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, help_text="Résumé du service")
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    content = RichTextField(blank=True)
    area_served = models.CharField(max_length=255, blank=True, help_text="Zone desservie (ville ou région)")
    is_featured = models.BooleanField(default=False, help_text="Mettre ce service en avant")

    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
        ('siblings_service_list', SiblingsServiceListBlock()),
        ('paginated_services', PaginatedServiceListBlock()),
        ('limited_services', LimitedServiceListBlock()),
    ], null=True, blank=True, use_json_field=True)  # Assure-toi que `use_json_field` est compatible avec ta version de Wagtail

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('summary'),
        FieldPanel('featured_image'),
        FieldPanel('content'),
        FieldPanel('area_served'),
        FieldPanel('is_featured'),
        FieldPanel('body'),
    ]

    def get_siblings_services(self, limit=3):
        siblings = ServicePage.objects.live().sibling_of(self).exclude(id=self.id)[:limit]
        return siblings if siblings.exists() else []

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request  # Ajout explicite de 'request' pour les blocs
        context['page'] = self  # Ajout explicite de 'page' pour les blocs
        return context

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class ServiceCategoryPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, help_text="Résumé de la catégorie")
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    content = RichTextField(blank=True)

    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
        ('paginated_services', PaginatedServiceListBlock()),
        ('limited_services', LimitedServiceListBlock()),
        ('siblings_service_list', SiblingsServiceListBlock()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('summary'),
        FieldPanel('featured_image'),
        FieldPanel('content'),
        FieldPanel('body'),
    ]

    def get_siblings_services(self, limit=3):
        # Méthode pour obtenir les catégories sœurs (même parent)
        siblings = ServiceCategoryPage.objects.live().sibling_of(self).exclude(id=self.id)[:limit]
        return siblings if siblings.exists() else []

    def get_services_list(self, request):
        services = ServicePage.objects.live().descendant_of(self).order_by('-first_published_at')
        return services

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request  # Ajout explicite de 'request' pour les blocs
        context['page'] = self  # Ajout explicite de 'page' pour les blocs
        return context

    class Meta:
        verbose_name = "Catégorie de service"
        verbose_name_plural = "Catégories de services"