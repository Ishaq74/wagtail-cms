"""
Enhanced streamfield blocks using the new base architecture.

This module provides improved, standardized blocks with better functionality,
consistency, and maintainability.
"""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock

from .base import (
    BaseContentBlock, 
    BaseListBlock, 
    DesignMixin, 
    ResponsiveImageMixin,
    LinkMixin,
    AccessibilityMixin,
    AnimationMixin
)


class HeadingBlock(BaseContentBlock):
    """Enhanced heading block with improved typography options."""
    
    heading_text = blocks.CharBlock(
        required=True, 
        help_text="Heading text"
    )
    
    heading_level = blocks.ChoiceBlock(
        choices=[
            ('h1', 'H1 - Main Title'),
            ('h2', 'H2 - Section Title'),
            ('h3', 'H3 - Subsection Title'),
            ('h4', 'H4 - Content Title'),
            ('h5', 'H5 - Minor Title'),
            ('h6', 'H6 - Small Title')
        ], 
        default='h2',
        help_text="Semantic heading level"
    )
    
    size = blocks.ChoiceBlock(
        choices=[
            ('xs', 'Extra Small'),
            ('sm', 'Small'),
            ('base', 'Base'),
            ('lg', 'Large'),
            ('xl', 'Extra Large'),
            ('2xl', '2X Large'),
            ('3xl', '3X Large'),
            ('4xl', '4X Large'),
            ('5xl', '5X Large'),
            ('6xl', '6X Large')
        ],
        default='base',
        help_text="Visual size (independent of semantic level)"
    )
    
    font_weight = blocks.ChoiceBlock(
        choices=[
            ('light', 'Light'),
            ('normal', 'Normal'),
            ('medium', 'Medium'),
            ('semibold', 'Semi Bold'),
            ('bold', 'Bold'),
            ('extrabold', 'Extra Bold')
        ],
        default='bold',
        help_text="Font weight"
    )
    
    class Meta:
        template = "streams/enhanced/heading_block.html"
        icon = "title"
        label = "Heading"


class ParagraphBlock(BaseContentBlock):
    """Enhanced paragraph block with rich text options."""
    
    text = blocks.RichTextBlock(
        required=True,
        features=['bold', 'italic', 'link', 'ol', 'ul', 'hr'],
        help_text="Paragraph content with basic formatting"
    )
    
    lead = blocks.BooleanBlock(
        required=False,
        help_text="Make this a lead paragraph (larger, emphasized text)"
    )
    
    class Meta:
        template = "streams/enhanced/paragraph_block.html"
        icon = "doc-full"
        label = "Paragraph"


class ImageBlock(BaseContentBlock, ResponsiveImageMixin):
    """Enhanced image block with modern responsive features."""
    
    caption = blocks.CharBlock(
        required=False,
        max_length=200,
        help_text="Image caption (optional)"
    )
    
    link = blocks.URLBlock(
        required=False,
        help_text="Make image clickable (optional)"
    )
    
    class Meta:
        template = "streams/enhanced/image_block.html"
        icon = "image"
        label = "Image"


class ButtonBlock(BaseContentBlock, LinkMixin):
    """Enhanced button block with comprehensive styling options."""
    
    text = blocks.CharBlock(
        required=True,
        max_length=50,
        help_text="Button text"
    )
    
    style = blocks.ChoiceBlock(
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('accent', 'Accent'),
            ('outline', 'Outline'),
            ('ghost', 'Ghost'),
            ('link', 'Link Style')
        ],
        default='primary',
        help_text="Button style"
    )
    
    size = blocks.ChoiceBlock(
        choices=[
            ('xs', 'Extra Small'),
            ('sm', 'Small'),
            ('md', 'Medium'),
            ('lg', 'Large'),
            ('xl', 'Extra Large')
        ],
        default='md',
        help_text="Button size"
    )
    
    full_width = blocks.BooleanBlock(
        required=False,
        help_text="Make button full width"
    )
    
    icon = blocks.ChoiceBlock(
        choices=[
            ('', 'No Icon'),
            ('arrow-right', 'Arrow Right'),
            ('arrow-left', 'Arrow Left'),
            ('download', 'Download'),
            ('external-link', 'External Link'),
            ('mail', 'Email'),
            ('phone', 'Phone'),
            ('play', 'Play'),
            ('chevron-right', 'Chevron Right'),
            ('plus', 'Plus')
        ],
        default='',
        required=False,
        help_text="Optional icon"
    )
    
    icon_position = blocks.ChoiceBlock(
        choices=[
            ('left', 'Left'),
            ('right', 'Right')
        ],
        default='right',
        help_text="Icon position"
    )
    
    class Meta:
        template = "streams/enhanced/button_block.html"
        icon = "link"
        label = "Button"


class ButtonGroupBlock(BaseContentBlock):
    """Enhanced button group with flexible layout."""
    
    buttons = blocks.ListBlock(
        ButtonBlock(),
        min_num=1,
        max_num=5,
        help_text="Add up to 5 buttons"
    )
    
    layout = blocks.ChoiceBlock(
        choices=[
            ('horizontal', 'Horizontal'),
            ('vertical', 'Vertical'),
            ('grid', 'Grid (auto-wrap)')
        ],
        default='horizontal',
        help_text="Button group layout"
    )
    
    gap = blocks.ChoiceBlock(
        choices=[
            ('xs', 'Extra Small'),
            ('sm', 'Small'),
            ('md', 'Medium'),
            ('lg', 'Large'),
            ('xl', 'Extra Large')
        ],
        default='md',
        help_text="Space between buttons"
    )
    
    class Meta:
        template = "streams/enhanced/button_group_block.html"
        icon = "link"
        label = "Button Group"


class GalleryBlock(BaseContentBlock):
    """Enhanced gallery with modern layout options."""
    
    images = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(required=True)),
            ('alt_text', blocks.CharBlock(required=False, max_length=255)),
            ('caption', blocks.CharBlock(required=False, max_length=200)),
        ]),
        min_num=2,
        help_text="Add images to the gallery"
    )
    
    layout = blocks.ChoiceBlock(
        choices=[
            ('grid', 'Grid Layout'),
            ('masonry', 'Masonry Layout'),
            ('carousel', 'Carousel'),
            ('slider', 'Slider with Controls')
        ],
        default='grid',
        help_text="Gallery layout style"
    )
    
    columns = blocks.ChoiceBlock(
        choices=[
            ('1', '1 Column'),
            ('2', '2 Columns'),
            ('3', '3 Columns'),
            ('4', '4 Columns'),
            ('auto', 'Auto (responsive)')
        ],
        default='auto',
        help_text="Number of columns (for grid layout)"
    )
    
    aspect_ratio = blocks.ChoiceBlock(
        choices=[
            ('auto', 'Auto'),
            ('square', 'Square (1:1)'),
            ('landscape', 'Landscape (4:3)'),
            ('wide', 'Wide (16:9)')
        ],
        default='auto',
        help_text="Force aspect ratio for all images"
    )
    
    enable_lightbox = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text="Enable lightbox for image viewing"
    )
    
    class Meta:
        template = "streams/enhanced/gallery_block.html"
        icon = "image"
        label = "Gallery"


class EmbedBlock(BaseContentBlock):
    """Enhanced embed block for external content."""
    
    embed = EmbedBlock(
        required=True,
        help_text="Embed external content (YouTube, Vimeo, etc.)"
    )
    
    caption = blocks.CharBlock(
        required=False,
        max_length=200,
        help_text="Optional caption for the embed"
    )
    
    aspect_ratio = blocks.ChoiceBlock(
        choices=[
            ('auto', 'Auto'),
            ('16:9', 'Widescreen (16:9)'),
            ('4:3', 'Standard (4:3)'),
            ('1:1', 'Square (1:1)')
        ],
        default='16:9',
        help_text="Aspect ratio for responsive embed"
    )
    
    class Meta:
        template = "streams/enhanced/embed_block.html"
        icon = "media"
        label = "Embed"


class QuoteBlock(BaseContentBlock):
    """Enhanced quote block with attribution options."""
    
    quote = blocks.TextBlock(
        required=True,
        help_text="Quote text"
    )
    
    author = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Quote author (optional)"
    )
    
    author_title = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Author title or affiliation (optional)"
    )
    
    style = blocks.ChoiceBlock(
        choices=[
            ('default', 'Default'),
            ('large', 'Large Quote'),
            ('bordered', 'Bordered'),
            ('highlighted', 'Highlighted Background')
        ],
        default='default',
        help_text="Quote styling"
    )
    
    class Meta:
        template = "streams/enhanced/quote_block.html"
        icon = "openquote"
        label = "Quote"


class CallToActionBlock(BaseContentBlock):
    """Enhanced call-to-action block."""
    
    heading = blocks.CharBlock(
        required=True,
        max_length=100,
        help_text="CTA heading"
    )
    
    description = blocks.TextBlock(
        required=False,
        help_text="Optional description text"
    )
    
    button = blocks.StreamBlock([
        ('button', ButtonBlock())
    ], 
    min_num=1, 
    max_num=2,
    help_text="Add 1-2 action buttons"
    )
    
    background_style = blocks.ChoiceBlock(
        choices=[
            ('none', 'No Background'),
            ('light', 'Light Background'),
            ('dark', 'Dark Background'),
            ('primary', 'Primary Color'),
            ('gradient', 'Gradient Background')
        ],
        default='light',
        help_text="Background styling"
    )
    
    class Meta:
        template = "streams/enhanced/cta_block.html"
        icon = "pick"
        label = "Call to Action"


# Layout Blocks

class ContainerBlock(BaseContentBlock):
    """Enhanced container block with flexible content."""
    
    content = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', ParagraphBlock()),
        ('image', ImageBlock()),
        ('button', ButtonBlock()),
        ('button_group', ButtonGroupBlock()),
        ('gallery', GalleryBlock()),
        ('embed', EmbedBlock()),
        ('quote', QuoteBlock()),
        ('cta', CallToActionBlock()),
        ('richtext', blocks.RichTextBlock()),
        ('document', DocumentChooserBlock()),
    ], 
    help_text="Add content blocks to this container"
    )
    
    container_width = blocks.ChoiceBlock(
        choices=[
            ('full', 'Full Width'),
            ('wide', 'Wide Container'),
            ('standard', 'Standard Container'),
            ('narrow', 'Narrow Container')
        ],
        default='standard',
        help_text="Container width"
    )
    
    background = blocks.ChoiceBlock(
        choices=[
            ('none', 'No Background'),
            ('light', 'Light Background'),
            ('dark', 'Dark Background'),
            ('primary', 'Primary Color'),
            ('image', 'Background Image')
        ],
        default='none',
        help_text="Container background"
    )
    
    background_image = ImageChooserBlock(
        required=False,
        help_text="Background image (if background is set to 'image')"
    )
    
    class Meta:
        template = "streams/enhanced/container_block.html"
        icon = "doc-empty"
        label = "Container"


class ColumnBlock(BaseContentBlock):
    """Enhanced multi-column layout block."""
    
    columns = blocks.StreamBlock([
        ('column', blocks.StreamBlock([
            ('heading', HeadingBlock()),
            ('paragraph', ParagraphBlock()),
            ('image', ImageBlock()),
            ('button', ButtonBlock()),
            ('button_group', ButtonGroupBlock()),
            ('gallery', GalleryBlock()),
            ('embed', EmbedBlock()),
            ('quote', QuoteBlock()),
            ('richtext', blocks.RichTextBlock()),
        ]))
    ], 
    min_num=2,
    max_num=4,
    help_text="Add 2-4 columns"
    )
    
    column_layout = blocks.ChoiceBlock(
        choices=[
            ('equal', 'Equal Width Columns'),
            ('2-1', '2:1 Ratio (2 columns)'),
            ('1-2', '1:2 Ratio (2 columns)'),
            ('1-2-1', '1:2:1 Ratio (3 columns)'),
            ('auto', 'Auto Width')
        ],
        default='equal',
        help_text="Column width distribution"
    )
    
    gap = blocks.ChoiceBlock(
        choices=[
            ('none', 'No Gap'),
            ('sm', 'Small Gap'),
            ('md', 'Medium Gap'),
            ('lg', 'Large Gap'),
            ('xl', 'Extra Large Gap')
        ],
        default='md',
        help_text="Gap between columns"
    )
    
    vertical_alignment = blocks.ChoiceBlock(
        choices=[
            ('top', 'Top'),
            ('center', 'Center'),
            ('bottom', 'Bottom'),
            ('stretch', 'Stretch')
        ],
        default='top',
        help_text="Vertical alignment of columns"
    )
    
    class Meta:
        template = "streams/enhanced/column_block.html"
        icon = "table"
        label = "Columns"