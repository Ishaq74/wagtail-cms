from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from streams import blocks as custom_blocks
from service.blocks import PaginatedServiceListBlock, LimitedServiceListBlock

from django.db import models

class HomePage(Page):
    max_count = 1
    # Utilisation de SingleColumnBlock qui accepte tous les blocs
    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
        ('paginated_services', PaginatedServiceListBlock()),
        ('limited_services', LimitedServiceListBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    page_description = "Ce type de page est destiné UNIQUEMENT à créer la page d'accueil."

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'