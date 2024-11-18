from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.images.blocks import ImageChooserBlock
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from streams import blocks as custom_blocks

class ServiceIndexPage(Page):
    max_count = 1
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, help_text="Résumé affiché en haut de la page")
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
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('summary'),
        FieldPanel('body'),
    ]

    page_description = "Page d'accueil des services"

    subpage_types = ['ServiceCategoryPage']
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request
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
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('summary'),
        FieldPanel('featured_image'),
        FieldPanel('content'),
        FieldPanel('body'),
    ]

    page_description = "Catégorie pour organiser les services"

    subpage_types = ['ServicePage', 'ServiceCategoryPage']
    parent_page_types = ['ServiceIndexPage', 'ServiceCategoryPage']

    class Meta:
        verbose_name = "Catégorie de service"
        verbose_name_plural = "Catégories de services"

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
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('summary'),
        FieldPanel('featured_image'),
        FieldPanel('content'),
        FieldPanel('area_served'),
        FieldPanel('is_featured'),
        FieldPanel('body'),
    ]

    parent_page_types = ['ServiceCategoryPage']
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context['request'] = request  # Ajout explicite de 'request' pour les blocs
        context['page'] = self  # Ajout explicite de 'page' pour les blocs
        return context

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"