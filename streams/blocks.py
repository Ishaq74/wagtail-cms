from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock

class AlignmentMixin(blocks.StructBlock):
    """Mixin pour ajouter l'alignement au bloc"""
    alignment = blocks.ChoiceBlock(choices=[
        ('left', 'Gauche'),
        ('center', 'Centre'),
        ('right', 'Droite')
    ], default='left', help_text="Choisir l'alignement du texte")

class ColorMixin(blocks.StructBlock):
    """Mixin pour ajouter la couleur au bloc"""
    color = blocks.ChoiceBlock(choices=[
        ('primary', 'Primary'),
        ('primary-light', 'Primary Light'),
        ('primary-dark', 'Primary Dark'),
        ('secondary', 'Secondary'),
        ('secondary-light', 'Secondary Light'),
        ('secondary-dark', 'Secondary Dark'),
        ('accent', 'Accent'),
        ('accent-light', 'Accent Light'),
        ('accent-dark', 'Accent Dark'),
        ('dark', 'Dark'),
        ('light', 'Light')
    ], default='dark', help_text="Choisir la couleur du texte")
    
class SpacingMixin(blocks.StructBlock):
    """Mixin pour ajouter l'espacement au bloc"""
    spacing = blocks.ChoiceBlock(choices=[
        ('normal', 'Espacement normal'),
        ('large', 'Grand espacement')
    ], default='normal', help_text="Choisir l'espacement entre les éléments")

    
class HeadingBlock(AlignmentMixin, ColorMixin, SpacingMixin, blocks.StructBlock):
    """Bloc de titre avec options d'alignement, couleur et espacement héritées des mixins"""
    heading_text = blocks.CharBlock(required=True, help_text="Ajouter le texte du titre")
    heading_level = blocks.ChoiceBlock(choices=[
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6')
    ], default='h2', help_text="Choisir le niveau du titre")

    class Meta:
        template = "streams/heading_block.html"
        icon = "title"
        label = "Titre"


    class Meta:
        template = "streams/heading_block.html"
        icon = "title"
        label = "Titre"

class ParagraphBlock(AlignmentMixin, ColorMixin, SpacingMixin, blocks.StructBlock):
    """Bloc de paragraphe avec options d'alignement, couleur et espacement"""
    text = blocks.TextBlock(required=True, help_text="Ajouter le texte du paragraphe")

    class Meta:
        template = "streams/paragraph_block.html"
        icon = "doc-full"
        label = "Paragraphe"

class SingleButtonBlock(blocks.StructBlock):
    """Bloc pour un seul bouton"""
    text = blocks.CharBlock(required=True, help_text="Texte du bouton")
    
    link = blocks.PageChooserBlock(required=False, help_text="Sélectionner une page interne")
    url = blocks.URLBlock(required=False, help_text="Ou entrer une URL externe (si aucune page n'est sélectionnée)")
    
    style = blocks.ChoiceBlock(choices=[
        ('btn-primary', 'Primary'),
        ('btn-secondary', 'Secondary'),
        ('btn-accent', 'Accent')
    ], default='btn-primary', help_text="Choisir le style du bouton")

    class Meta:
        template = None  # Pas besoin de template ici, géré dans ButtonGroupBlock
        icon = "link"
        label = "Bouton"

class ButtonGroupBlock(blocks.ListBlock):
    """Bloc qui permet d'ajouter plusieurs boutons"""
    def __init__(self, **kwargs):
        super().__init__(SingleButtonBlock(), **kwargs)

    class Meta:
        template = "streams/button_group_block.html"  # Template pour afficher tous les boutons
        icon = "link"
        label = "Groupe de Boutons"


class ImageBlock(AlignmentMixin, SpacingMixin, blocks.StructBlock):
    """Bloc d'image avec options d'alignement, taille, alt et chargement"""
    image = ImageChooserBlock(required=True, help_text="Choisir une image")
    alt_text = blocks.CharBlock(required=False, blank=True, max_length=255, help_text="Texte alternatif pour l'image")
    
    # Choix de la taille de l'image
    size = blocks.ChoiceBlock(choices=[
        ('small', 'Petite'),
        ('medium', 'Moyenne'),
        ('large', 'Grande')
    ], default='medium', help_text="Choisir la taille de l'image")
    
    # Option pour le chargement des images
    loading = blocks.ChoiceBlock(choices=[
        ('lazy', 'Lazy (différé)'),
        ('eager', 'Eager (immédiat)')
    ], default='lazy', help_text="Choisir la méthode de chargement de l'image")

    class Meta:
        template = "streams/image_block.html"
        icon = "image"
        label = "Image"

class GalleryBlock(blocks.StructBlock):
    """Bloc de galerie avec différents styles de présentation"""
    images = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(required=True, help_text="Choisir une image")),
            ('alt_text', blocks.CharBlock(required=False, max_length=255, help_text="Texte alternatif pour l'image")),
        ])
    )
    
    style = blocks.ChoiceBlock(choices=[
        ('default', 'Disposition par défaut'),
        ('carousel', 'Carrousel'),
        ('slider', 'Slider'),
        ('photography', 'Photography'),
    ], default='default', help_text="Choisir le style de galerie")

    class Meta:
        template = "streams/gallery_block.html"
        icon = "image"
        label = "Galerie"

class SingleColumnBlock(blocks.StreamBlock):
    """Bloc de section en une seule colonne qui accepte tous les types de blocs."""

    # Blocs personnalisés que nous avons créés
    heading = HeadingBlock()
    paragraph = ParagraphBlock()
    buttons = ButtonGroupBlock()
    image = ImageBlock()
    Gallery = GalleryBlock()

    # Blocs natifs de Wagtail avec Wagtail 6.2 support
    richtext = blocks.RichTextBlock()
    document = DocumentChooserBlock(required=False, label="Document")
    embed = EmbedBlock(help_text="Ajouter un média externe (vidéo, audio, etc.)")

    # Et tous les autres blocs de base de Wagtail
    quote = blocks.BlockQuoteBlock()
    list = blocks.ListBlock(blocks.CharBlock(label="Item de liste"))

    class Meta:
        template = "streams/single_column_block.html"
        icon = "placeholder"
        label = "Section à une colonne"

class DoubleColumnBlock(blocks.StructBlock):
    """Bloc Double Colonne avec RichText au-dessus et blocs dans chaque colonne."""
    
    rich_text = blocks.RichTextBlock(required=False, help_text="Ajouter un texte ou une description avant les colonnes")
    
    left_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', ParagraphBlock()),
        ('buttons', ButtonGroupBlock()),
        ('image', ImageBlock()),
        ('gallery', GalleryBlock()),
        ('richtext', blocks.RichTextBlock()),
        ('document', DocumentChooserBlock(required=False, label="Document")),
        ('embed', EmbedBlock(help_text="Ajouter un média externe (vidéo, audio, etc.)")),
        ('quote', blocks.BlockQuoteBlock()),
        ('list', blocks.ListBlock(blocks.CharBlock(label="Item de liste"))),
    ], required=False, help_text="Ajouter des blocs à la colonne gauche")

    right_column = blocks.StreamBlock([
        ('heading', HeadingBlock()),
        ('paragraph', ParagraphBlock()),
        ('buttons', ButtonGroupBlock()),
        ('image', ImageBlock()),
        ('gallery', GalleryBlock()),
        ('richtext', blocks.RichTextBlock()),
        ('document', DocumentChooserBlock(required=False, label="Document")),
        ('embed', EmbedBlock(help_text="Ajouter un média externe (vidéo, audio, etc.)")),
        ('quote', blocks.BlockQuoteBlock()),
        ('list', blocks.ListBlock(blocks.CharBlock(label="Item de liste"))),
    ], required=False, help_text="Ajouter des blocs à la colonne droite")

    class Meta:
        template = "streams/double_column_block.html"
        icon = "placeholder"
        label = "Double Colonne"