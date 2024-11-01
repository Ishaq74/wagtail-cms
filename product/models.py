from django import forms
from django.db import models
from wagtail.admin.panels import (
    FieldPanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel, InlinePanel
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail import blocks
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from streams import blocks as custom_blocks  # Si vous utilisez des blocs personnalisés

@register_snippet
class ProductVariant(ClusterableModel):
    name = models.CharField(
        max_length=255, help_text="Nom de la variante (par ex. Taille, Couleur)"
    )

    panels = [
        FieldPanel('name'),
        InlinePanel('options', label="Options"),
    ]

    def __str__(self):
        return self.name

class VariantOption(models.Model):
    variant = ParentalKey('ProductVariant', related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Nom de l'option (par ex. Petit, Moyen, Grand)")
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    additional_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Prix supplémentaire pour cette option (si applicable)"
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('image'),
        FieldPanel('additional_price'),
    ]

    def __str__(self):
        return self.name

class ProductCategory(Page):
    summary = RichTextField(blank=True)
    content = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    is_featured = models.BooleanField(default=False)

    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('content'),
        FieldPanel('featured_image'),
        FieldPanel('is_featured'),
        FieldPanel('body'),
    ]

    subpage_types = ['product.ProductCategory', 'product.ProductPage']
    parent_page_types = ['home.HomePage', 'product.ProductCategory']

    def __str__(self):
        return self.title

class ProductPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProductPage', related_name='tagged_items', on_delete=models.CASCADE
    )

class ProductVariantChoiceBlock(blocks.StructBlock):
    variant = SnippetChooserBlock('product.ProductVariant', required=True)

    class Meta:
        icon = 'list-ul'
        label = 'Variante du produit'

class ProductPage(Page):
    summary = RichTextField(blank=True)
    content = RichTextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    categories = ParentalManyToManyField('product.ProductCategory', blank=True)
    tags = ClusterTaggableManager(through=ProductPageTag, blank=True)
    variants = StreamField(
        [('variant', ProductVariantChoiceBlock())],
        null=True, blank=True, use_json_field=True
    )

    body = StreamField([
        ('single_column', custom_blocks.SingleColumnBlock()),
        ('double_column', custom_blocks.DoubleColumnBlock()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('content'),
        FieldPanel('featured_image'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('price'),
                FieldPanel('sku'),
            ]),
            FieldRowPanel([
                FieldPanel('is_available'),
                FieldPanel('is_featured'),
            ]),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading="Détails du produit"),
        FieldPanel('variants'),
        FieldPanel('body'),
        # Votre StreamField pour la galerie d'images, que nous ne modifions pas
    ]

    parent_page_types = ['product.ProductCategory']
    subpage_types = []

    def __str__(self):
        return self.title
