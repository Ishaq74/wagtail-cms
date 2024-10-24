from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from streams import blocks as custom_blocks  # Import des blocs personnalisés

class FlexPage(Page):
    # Utilisation de SingleColumnBlock qui accepte tous les blocs
    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    page_description = "Ce type de page est destiné aux pages indépendantes (À propos, contact, etc.)"

    class Meta:
        verbose_name = 'Flex Page'
        verbose_name_plural = 'Flex Pages'
