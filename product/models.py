from django import forms
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail import blocks
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from streams import blocks as custom_blocks  # Utilisé pour les blocs personnalisés
from taxes.models import TaxProduct

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
    stock_quantity = models.PositiveIntegerField(default=0)  # Stock spécifique pour la variante
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
        FieldPanel('stock_quantity'),
    ]

    def __str__(self):
        return self.name

class ProductIndexPage(Page):
    max_count = 1
    intro = RichTextField(blank=True, help_text="Introduction de la page des produits")

    body = StreamField(
        [
            ('paginated_product_list', custom_blocks.PaginatedProductListBlock()),
            ('limited_product_list', custom_blocks.LimitedProductListBlock()),
            ('paginated_product_category_list', custom_blocks.PaginatedProductCategoryListBlock()),
            ('limited_product_category_list', custom_blocks.LimitedProductCategoryListBlock()),
            ('paginated_blog_list', custom_blocks.PaginatedBlogListBlock()),
            ('limited_blog_list', custom_blocks.LimitedBlogListBlock()),
            ('paginated_blog_category_list', custom_blocks.PaginatedBlogCategoryListBlock()),
            ('limited_blog_category_list', custom_blocks.LimitedBlogCategoryListBlock()),
            ('single_column', custom_blocks.SingleColumnBlock()),
            ('double_column', custom_blocks.DoubleColumnBlock()),
        ],
        null=True, blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    subpage_types = ['product.ProductCategory', 'product.ProductPage']
    parent_page_types = ['home.HomePage']

    page_description = "Page d'accueil de la Boutique"

    class Meta:
        verbose_name = "Boutique"
    def get_context(self, request):
        context = super().get_context(request)
        product_categories = self.get_children().live().type(ProductCategory).order_by('first_published_at')
        paginator = Paginator(product_categories, 12)
        page = request.GET.get('page')
        try:
            categories_paginated = paginator.page(page)
        except PageNotAnInteger:
            categories_paginated = paginator.page(1)
        except EmptyPage:
            categories_paginated = paginator.page(paginator.num_pages)
            
        featured_products = ProductPage.objects.live().filter(is_featured=True).order_by('first_published_at')[:6]

        context['product_categories'] = categories_paginated
        context['pagination'] = categories_paginated
        context['featured_products'] = featured_products
        return context

class ProductCategory(Page):
    summary = RichTextField(blank=True)
    content = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    is_featured = models.BooleanField(default=False)

    body = StreamField(
        [
            ('single_column', custom_blocks.SingleColumnBlock()),
            ('double_column', custom_blocks.DoubleColumnBlock()),
        ],
        null=True, blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('content'),
        FieldPanel('featured_image'),
        FieldPanel('is_featured'),
        FieldPanel('body'),
    ]

    subpage_types = ['product.ProductCategory', 'product.ProductPage']
    parent_page_types = ['product.ProductIndexPage','product.ProductCategory']

    page_description = "Créer une catégorie de produits."

    def __str__(self):
        return self.title
    def is_category(self):
        return True

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
    tax_included = models.BooleanField(default=False)
    tax_product = models.ForeignKey('taxes.TaxProduct', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=255, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    categories = ParentalManyToManyField('product.ProductCategory', blank=True)
    tags = ClusterTaggableManager(through=ProductPageTag, blank=True)
    variants = StreamField(
        [('variant', ProductVariantChoiceBlock())],
        null=True, blank=True, use_json_field=True
    )

    body = StreamField(
        [
            ('single_column', custom_blocks.SingleColumnBlock()),
            ('double_column', custom_blocks.DoubleColumnBlock()),
        ],
        null=True, blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('content'),
        FieldPanel('featured_image'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('price'),
                FieldPanel('tax_included'),
                FieldPanel('tax_product'),
                FieldPanel('sku'),
            ]),
            FieldRowPanel([
                FieldPanel('is_available'),
                FieldPanel('stock_quantity'),
                FieldPanel('is_featured'),
            ]),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading="Détails du produit"),
        FieldPanel('variants'),
        FieldPanel('body'),
    ]

    parent_page_types = ['product.ProductCategory']
    subpage_types = []

    page_description = "Créer un produit."

    def __str__(self):
        return self.title

    def is_product(self):
        return True
    
    @property
    def is_out_of_stock(self):
        return self.stock_quantity == 0