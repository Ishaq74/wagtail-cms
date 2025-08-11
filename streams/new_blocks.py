"""
New standardized blocks architecture for Wagtail CMS.

This module provides the new EXTRAORDINARY streamfield system with:
- Standardized base classes and mixins
- Consistent patterns and naming
- Reduced code duplication
- Enhanced functionality
- Better maintainability

This replaces the original blocks.py with a more organized, scalable approach.
"""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock

# Import our enhanced block system
from .enhanced_blocks import (
    HeadingBlock,
    ParagraphBlock,
    ImageBlock,
    ButtonBlock,
    ButtonGroupBlock,
    GalleryBlock,
    EmbedBlock as EnhancedEmbedBlock,
    QuoteBlock,
    CallToActionBlock,
    ContainerBlock,
    ColumnBlock
)

from .list_blocks import (
    ProductListBlock,
    BlogListBlock, 
    ServiceListBlock,
    BusinessListBlock,
    ProductCategoryListBlock,
    BlogCategoryListBlock,
    ServiceCategoryListBlock,
    BusinessCategoryListBlock
)

# Legacy compatibility - keeping some of the original block names
# but implemented with the new architecture

class LegacyHeadingBlock(HeadingBlock):
    """Legacy compatibility for original HeadingBlock."""
    class Meta:
        template = "streams/heading_block.html"
        icon = "title"
        label = "Titre"


class LegacyParagraphBlock(ParagraphBlock):
    """Legacy compatibility for original ParagraphBlock."""
    class Meta:
        template = "streams/paragraph_block.html" 
        icon = "doc-full"
        label = "Paragraphe"


class LegacyImageBlock(ImageBlock):
    """Legacy compatibility for original ImageBlock."""
    class Meta:
        template = "streams/image_block.html"
        icon = "image"
        label = "Image"


class LegacyGalleryBlock(GalleryBlock):
    """Legacy compatibility for original GalleryBlock."""
    class Meta:
        template = "streams/gallery_block.html"
        icon = "image"
        label = "Galerie"


# Enhanced StreamBlocks for common layouts

class FlexibleStreamBlock(blocks.StreamBlock):
    """Main flexible stream block with all available content types."""
    
    # Content Blocks
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    image = ImageBlock()
    gallery = GalleryBlock()
    quote = QuoteBlock()
    embed = EnhancedEmbedBlock()
    
    # Interactive Blocks
    button = ButtonBlock()
    button_group = ButtonGroupBlock()
    cta = CallToActionBlock()
    
    # Layout Blocks
    container = ContainerBlock()
    columns = ColumnBlock()
    
    # List Blocks (dynamically created)
    product_list = ProductListBlock()
    blog_list = BlogListBlock()
    service_list = ServiceListBlock()
    business_list = BusinessListBlock()
    
    # Category List Blocks
    product_categories = ProductCategoryListBlock()
    blog_categories = BlogCategoryListBlock()
    service_categories = ServiceCategoryListBlock()
    business_categories = BusinessCategoryListBlock()
    
    # Native Wagtail Blocks (enhanced)
    richtext = blocks.RichTextBlock(
        features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link'],
        help_text="Rich text with enhanced formatting options"
    )
    document = DocumentChooserBlock(
        required=False,
        help_text="Link to a document"
    )
    
    class Meta:
        template = "streams/enhanced/flexible_stream_block.html"
        icon = "doc-empty"
        label = "Flexible Content"


class SingleColumnBlock(FlexibleStreamBlock):
    """Single column layout block (enhanced version of original)."""
    
    class Meta:
        template = "streams/single_column_block.html"
        icon = "doc-empty"
        label = "Section Grid"


class DoubleColumnBlock(ColumnBlock):
    """Enhanced double column block."""
    
    def __init__(self, **kwargs):
        # Override to ensure exactly 2 columns
        super().__init__(**kwargs)
        self.child_blocks['columns'].min_num = 2
        self.child_blocks['columns'].max_num = 2
    
    class Meta:
        template = "streams/double_column_block.html"
        icon = "table"
        label = "Section Grid 2"


# Specialized blocks for specific use cases

class HeroBlock(blocks.StructBlock):
    """Enhanced hero block for landing pages."""
    
    heading = blocks.CharBlock(
        required=True,
        max_length=100,
        help_text="Main hero heading"
    )
    
    subheading = blocks.CharBlock(
        required=False,
        max_length=200,
        help_text="Optional subheading"
    )
    
    description = blocks.TextBlock(
        required=False,
        help_text="Hero description text"
    )
    
    background_image = ImageChooserBlock(
        required=False,
        help_text="Background image"
    )
    
    background_video = blocks.URLBlock(
        required=False,
        help_text="Background video URL (YouTube, Vimeo)"
    )
    
    overlay_opacity = blocks.ChoiceBlock(
        choices=[
            ('0', 'No Overlay'),
            ('25', 'Light Overlay'),
            ('50', 'Medium Overlay'),
            ('75', 'Dark Overlay'),
            ('90', 'Very Dark Overlay')
        ],
        default='50',
        help_text="Background overlay opacity"
    )
    
    text_alignment = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left'),
            ('center', 'Center'),
            ('right', 'Right')
        ],
        default='center',
        help_text="Text alignment"
    )
    
    text_color = blocks.ChoiceBlock(
        choices=[
            ('light', 'Light Text'),
            ('dark', 'Dark Text'),
            ('auto', 'Auto (based on background)')
        ],
        default='auto',
        help_text="Text color theme"
    )
    
    buttons = blocks.ListBlock(
        ButtonBlock(),
        min_num=0,
        max_num=3,
        help_text="Call-to-action buttons"
    )
    
    height = blocks.ChoiceBlock(
        choices=[
            ('sm', 'Small (400px)'),
            ('md', 'Medium (500px)'),
            ('lg', 'Large (600px)'),
            ('xl', 'Extra Large (700px)'),
            ('full', 'Full Screen'),
            ('auto', 'Auto Height')
        ],
        default='lg',
        help_text="Hero section height"
    )
    
    class Meta:
        template = "streams/enhanced/hero_block.html"
        icon = "image"
        label = "Hero Section"


class TestimonialBlock(blocks.StructBlock):
    """Enhanced testimonial block."""
    
    quote = blocks.TextBlock(
        required=True,
        help_text="Testimonial text"
    )
    
    author_name = blocks.CharBlock(
        required=True,
        max_length=100,
        help_text="Author name"
    )
    
    author_title = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Author title/position"
    )
    
    author_company = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Author company"
    )
    
    author_image = ImageChooserBlock(
        required=False,
        help_text="Author photo"
    )
    
    rating = blocks.IntegerBlock(
        required=False,
        min_value=1,
        max_value=5,
        help_text="Star rating (1-5)"
    )
    
    style = blocks.ChoiceBlock(
        choices=[
            ('card', 'Card Style'),
            ('minimal', 'Minimal Style'),
            ('featured', 'Featured Style')
        ],
        default='card',
        help_text="Testimonial styling"
    )
    
    class Meta:
        template = "streams/enhanced/testimonial_block.html"
        icon = "user"
        label = "Testimonial"


class AccordionBlock(blocks.StructBlock):
    """Enhanced accordion/FAQ block."""
    
    items = blocks.ListBlock(
        blocks.StructBlock([
            ('title', blocks.CharBlock(required=True, max_length=200)),
            ('content', blocks.RichTextBlock(required=True)),
            ('open_by_default', blocks.BooleanBlock(required=False))
        ]),
        min_num=1,
        help_text="Add accordion items"
    )
    
    style = blocks.ChoiceBlock(
        choices=[
            ('default', 'Default'),
            ('bordered', 'Bordered'),
            ('minimal', 'Minimal'),
            ('colored', 'Colored Headers')
        ],
        default='default',
        help_text="Accordion styling"
    )
    
    allow_multiple = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text="Allow multiple items to be open at once"
    )
    
    class Meta:
        template = "streams/enhanced/accordion_block.html"
        icon = "list-ol"
        label = "Accordion/FAQ"


# Opening hours block (enhanced version)
class OpeningHoursBlock(blocks.StructBlock):
    """Enhanced opening hours block."""
    
    business_name = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Business name (optional)"
    )
    
    hours = blocks.ListBlock(
        blocks.StructBlock([
            ('day', blocks.ChoiceBlock(choices=[
                ('monday', 'Monday'),
                ('tuesday', 'Tuesday'), 
                ('wednesday', 'Wednesday'),
                ('thursday', 'Thursday'),
                ('friday', 'Friday'),
                ('saturday', 'Saturday'),
                ('sunday', 'Sunday'),
            ])),
            ('open_time', blocks.TimeBlock(required=False)),
            ('close_time', blocks.TimeBlock(required=False)),
            ('second_open_time', blocks.TimeBlock(required=False)),
            ('second_close_time', blocks.TimeBlock(required=False)),
            ('closed', blocks.BooleanBlock(required=False))
        ]),
        help_text="Add opening hours for each day"
    )
    
    timezone = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text="Timezone (e.g., 'Europe/Paris')"
    )
    
    special_note = blocks.CharBlock(
        required=False,
        max_length=200,
        help_text="Special note (e.g., 'Closed on holidays')"
    )
    
    style = blocks.ChoiceBlock(
        choices=[
            ('table', 'Table Format'),
            ('list', 'List Format'),
            ('compact', 'Compact Format')
        ],
        default='table',
        help_text="Display style"
    )
    
    class Meta:
        template = "streams/enhanced/opening_hours_block.html"
        icon = 'time'
        label = "Opening Hours"


# Main StreamBlock for pages
class MainStreamBlock(FlexibleStreamBlock):
    """Main stream block with all available blocks for page content."""
    
    # Add specialized blocks
    hero = HeroBlock()
    testimonial = TestimonialBlock()
    accordion = AccordionBlock()
    opening_hours = OpeningHoursBlock()
    
    class Meta:
        template = "streams/enhanced/main_stream_block.html"
        icon = "doc-full"
        label = "Page Content"