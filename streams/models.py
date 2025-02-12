from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock

class SingleColumnBlock(blocks.StreamBlock):
    """Single column block that allows any type of content."""
    richtext = RichTextBlock(required=False, help_text="Ajouter du texte enrichi")
    image = ImageChooserBlock(required=False, help_text="Ajouter une image")
    button = blocks.StructBlock([
        ('text', blocks.CharBlock(required=True, help_text="Texte du bouton")),
        ('url', blocks.URLBlock(required=True, help_text="Lien du bouton")),
    ], required=False, help_text="Ajouter un bouton")

    class Meta:
        template = "streams/single_column_block.html"
        icon = "placeholder"
        label = "Single Column"
