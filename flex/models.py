from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from streams import blocks as custom_blocks

class FlexPage(Page):
    body = StreamField([
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
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    page_description = "Ce type de page est destiné aux pages indépendantes (À propos, contact, etc.)"

    class Meta:
        verbose_name = 'Flex Page'
        verbose_name_plural = 'Flex Pages'
