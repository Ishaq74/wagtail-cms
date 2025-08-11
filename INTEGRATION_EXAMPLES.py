"""
Integration example showing how to use the new enhanced streamfields in page models.

This example demonstrates:
1. Upgrading existing page models to use new streamfields
2. Backward compatibility maintenance
3. Progressive enhancement approach
"""

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from django.db import models

# Import the new enhanced streamfield system
from streams.new_blocks import (
    MainStreamBlock,
    FlexibleStreamBlock,
    HeroBlock,
    TestimonialBlock
)

# Import configuration-driven list blocks
from streams.list_blocks import (
    ProductListBlock,
    BlogListBlock,
    ServiceListBlock
)


class EnhancedHomePage(Page):
    """
    Enhanced home page using the new EXTRAORDINARY streamfield system.
    
    This demonstrates the new architecture while maintaining compatibility.
    """
    
    # Hero section using specialized hero block
    hero = StreamField([
        ('hero', HeroBlock()),
    ], blank=True, help_text="Hero section for the homepage")
    
    # Main content using the comprehensive MainStreamBlock
    content = StreamField(
        MainStreamBlock(),
        blank=True,
        help_text="Main page content with all available blocks"
    )
    
    # Featured content using configuration-driven list blocks
    featured_products = StreamField([
        ('products', ProductListBlock()),
    ], blank=True, help_text="Featured products section")
    
    featured_blog_posts = StreamField([
        ('blog_posts', BlogListBlock()),
    ], blank=True, help_text="Featured blog posts section")
    
    # Testimonials section
    testimonials = StreamField([
        ('testimonial', TestimonialBlock()),
    ], blank=True, help_text="Customer testimonials")
    
    content_panels = Page.content_panels + [
        FieldPanel('hero'),
        FieldPanel('content'),
        FieldPanel('featured_products'),
        FieldPanel('featured_blog_posts'),
        FieldPanel('testimonials'),
    ]
    
    class Meta:
        verbose_name = "Enhanced Home Page"
        

class FlexibleContentPage(Page):
    """
    Flexible content page using the enhanced streamfield system.
    
    This is perfect for general content pages that need maximum flexibility.
    """
    
    # Use the flexible stream block for maximum versatility
    content = StreamField(
        FlexibleStreamBlock(),
        blank=True,
        help_text="Page content with flexible blocks"
    )
    
    # Optional sidebar content
    sidebar = StreamField([
        ('cta', CallToActionBlock()),
        ('testimonial', TestimonialBlock()),
        ('products', ProductListBlock()),
        ('services', ServiceListBlock()),
    ], blank=True, help_text="Sidebar content")
    
    content_panels = Page.content_panels + [
        FieldPanel('content'),
        FieldPanel('sidebar'),
    ]
    
    class Meta:
        verbose_name = "Flexible Content Page"


class LandingPage(Page):
    """
    Landing page optimized for conversions using specialized blocks.
    """
    
    # Hero section
    hero = StreamField([
        ('hero', HeroBlock()),
    ], max_num=1, help_text="Main hero section")
    
    # Main selling points
    selling_points = StreamField([
        ('heading', HeadingBlock()),
        ('paragraph', ParagraphBlock()),
        ('columns', ColumnBlock()),
        ('cta', CallToActionBlock()),
    ], blank=True, help_text="Key selling points")
    
    # Social proof
    social_proof = StreamField([
        ('testimonial', TestimonialBlock()),
        ('products', ProductListBlock()),  # For featured products
    ], blank=True, help_text="Social proof and testimonials")
    
    # FAQ section
    faq = StreamField([
        ('accordion', AccordionBlock()),
    ], blank=True, help_text="Frequently asked questions")
    
    # Final CTA
    bottom_cta = StreamField([
        ('cta', CallToActionBlock()),
    ], max_num=1, help_text="Final call-to-action")
    
    content_panels = Page.content_panels + [
        FieldPanel('hero'),
        FieldPanel('selling_points'),
        FieldPanel('social_proof'),
        FieldPanel('faq'),
        FieldPanel('bottom_cta'),
    ]
    
    class Meta:
        verbose_name = "Landing Page"


# Example of upgrading an existing model
class UpgradedBlogPage(Page):
    """
    Example of upgrading an existing blog page to use enhanced blocks.
    
    This shows how to maintain backward compatibility while adding new features.
    """
    
    # Keep existing fields for backward compatibility
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True)
    
    # Upgrade content field to use enhanced blocks
    # The old content will still work, but new content gets enhanced features
    body = StreamField([
        # Enhanced content blocks
        ('heading', HeadingBlock()),
        ('paragraph', ParagraphBlock()),
        ('image', ImageBlock()),
        ('quote', QuoteBlock()),
        ('gallery', GalleryBlock()),
        ('embed', EmbedBlock()),
        ('cta', CallToActionBlock()),
        ('accordion', AccordionBlock()),
        
        # Related content
        ('related_products', ProductListBlock()),
        ('related_services', ServiceListBlock()),
        ('related_posts', BlogListBlock()),
    ], blank=True)
    
    # New enhanced author info
    author_info = StreamField([
        ('testimonial', TestimonialBlock()),  # Can be used for author bio
    ], blank=True, help_text="Author information")
    
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('author_info'),
    ]


# Example of a specialized page using configuration-driven blocks
class ProductCatalogPage(Page):
    """
    Product catalog page using the configuration-driven list blocks.
    
    This demonstrates the power of the new list block system.
    """
    
    # Page header
    header = StreamField([
        ('hero', HeroBlock()),
        ('heading', HeadingBlock()),
        ('paragraph', ParagraphBlock()),
    ], blank=True, help_text="Page header content")
    
    # Main product listings - can have multiple sections
    product_sections = StreamField([
        ('products', ProductListBlock()),
        ('product_categories', ProductCategoryListBlock()),
    ], blank=True, help_text="Product listing sections")
    
    # Additional content
    content = StreamField([
        ('heading', HeadingBlock()),
        ('paragraph', ParagraphBlock()),
        ('cta', CallToActionBlock()),
        ('testimonial', TestimonialBlock()),
    ], blank=True, help_text="Additional content")
    
    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('product_sections'),
        FieldPanel('content'),
    ]
    
    class Meta:
        verbose_name = "Product Catalog Page"


# Import necessary blocks for the examples above
from streams.enhanced_blocks import (
    HeadingBlock,
    ParagraphBlock,
    ImageBlock,
    QuoteBlock,
    GalleryBlock,
    EmbedBlock,
    CallToActionBlock,
    ColumnBlock
)

from streams.new_blocks import (
    AccordionBlock,
)

from streams.list_blocks import (
    ProductCategoryListBlock,
)