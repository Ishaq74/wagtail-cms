from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
        ('h1', 'H1'),
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
        icon = "doc-empty"
        label = "SectionGrid"

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
        icon = "table"
        label = "SectionGrid2"
        
class PaginatedProductListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=6, help_text="Nombre de produits par page")
    categories = blocks.ListBlock(
        blocks.PageChooserBlock(target_model='product.ProductCategory'),
        required=False,
        help_text="Choisissez les catégories pour filtrer les produits"
    )

    def get_context(self, value, parent_context=None):
        from product.models import ProductPage
        context = super().get_context(value, parent_context)
        request = parent_context.get('request')
        categories = value['categories']
        
        products = ProductPage.objects.live()
        if categories:
            products = products.filter(categories__in=categories)

        paginator = Paginator(products.distinct(), value['limit'])
        page_number = request.GET.get('page')
        
        try:
            paginated_products = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)

        context['products'] = paginated_products
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste des Produits'
        template = 'product/paginated_product_list.html'

class LimitedProductListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de produits à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les produits vedettes")
    categories = blocks.ListBlock(
        blocks.PageChooserBlock(target_model='product.ProductCategory'),
        required=False,
        help_text="Choisissez les catégories pour filtrer les produits"
    )

    def get_context(self, value, parent_context=None):
        from product.models import ProductPage
        context = super().get_context(value, parent_context)
        
        products = ProductPage.objects.live()
        
        if value['featured_only']:
            products = products.filter(is_featured=True)
        if value['categories']:
            products = products.filter(categories__in=value['categories'])

        context['products'] = products.distinct()[:value['limit']]
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Featured Product'
        template = 'product/limited_product_list.html'

class LimitedProductCategoryListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de catégories de produits à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les catégories vedettes")

    def get_context(self, value, parent_context=None):
        from product.models import ProductCategory
        context = super().get_context(value, parent_context)

        product_categories = ProductCategory.objects.live()
        if value['featured_only']:
            product_categories = product_categories.filter(is_featured=True)

        context['product_categories'] = product_categories.distinct()[:value['limit']]
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Liste des Catégories de Produits'
        template = 'product/limited_product_category_list.html'

class PaginatedProductCategoryListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=6, help_text="Nombre de catégories de produits par page")

    def get_context(self, value, parent_context=None):
        from product.models import ProductCategory
        context = super().get_context(value, parent_context)

        request = parent_context.get('request')
        product_categories = ProductCategory.objects.live()

        paginator = Paginator(product_categories.distinct(), value['limit'])
        page_number = request.GET.get('page')

        try:
            paginated_product_categories = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_product_categories = paginator.page(1)
        except EmptyPage:
            paginated_product_categories = paginator.page(paginator.num_pages)

        context['product_categories'] = paginated_product_categories
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste des Catégories de Produits'
        template = 'product/paginated_product_category_list.html'

class PaginatedBlogListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre d'articles de blog par page")
    categories = blocks.ListBlock(
        blocks.PageChooserBlock(target_model='blog.BlogCategoryPage'),
        required=False,
        help_text="Choisissez les catégories pour filtrer les articles"
    )

    def get_context(self, value, parent_context=None):
        from blog.models import BlogPage
        context = super().get_context(value, parent_context)
        request = parent_context.get('request')
        categories = value['categories']

        # Filtrage des articles de blog
        blogpages = BlogPage.objects.live().order_by('-date')
        if categories:
            blogpages = blogpages.filter(categories__in=categories)

        # Pagination
        paginator = Paginator(blogpages.distinct(), value['limit'])
        page_number = request.GET.get('page')

        try:
            paginated_blogpages = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_blogpages = paginator.page(1)
        except EmptyPage:
            paginated_blogpages = paginator.page(paginator.num_pages)

        context['blogpages'] = paginated_blogpages
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste des Articles'
        template = 'blog/paginated_blog_list.html'

class LimitedBlogListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre d'articles de blog à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les articles en vedette")
    categories = blocks.ListBlock(
        blocks.PageChooserBlock(target_model='blog.BlogCategoryPage'),
        required=False,
        help_text="Choisissez les catégories pour filtrer les articles"
    )

    def get_context(self, value, parent_context=None):
        from blog.models import BlogPage
        context = super().get_context(value, parent_context)
        
        # Filtrage des articles de blog
        blogpages = BlogPage.objects.live().order_by('-date')
        if value['featured_only']:
            blogpages = blogpages.filter(is_featured=True)
        if value['categories']:
            blogpages = blogpages.filter(categories__in=value['categories'])

        context['blogpages'] = blogpages.distinct()[:value['limit']]
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Featured Articles'
        template = 'blog/limited_blog_list.html'

class PaginatedBlogCategoryListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de catégories de blog par page")

    def get_context(self, value, parent_context=None):
        from blog.models import BlogCategoryPage
        context = super().get_context(value, parent_context)
        request = parent_context.get('request')

        # Filtrage et pagination des catégories
        blogcategories = BlogCategoryPage.objects.live().order_by('title')
        paginator = Paginator(blogcategories.distinct(), value['limit'])
        page_number = request.GET.get('page')

        try:
            paginated_blogcategories = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_blogcategories = paginator.page(1)
        except EmptyPage:
            paginated_blogcategories = paginator.page(paginator.num_pages)

        context['blogcategories'] = paginated_blogcategories
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste des Catégories du Blog'
        template = 'blog/paginated_blog_category_list.html'

class LimitedBlogCategoryListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de catégories de blog à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les catégories en vedette")

    def get_context(self, value, parent_context=None):
        from blog.models import BlogCategoryPage
        context = super().get_context(value, parent_context)

        # Filtrage des catégories de blog
        blogcategories = BlogCategoryPage.objects.live()
        if value['featured_only']:
            blogcategories = blogcategories.filter(is_featured=True)

        context['blogcategories'] = blogcategories.distinct()[:value['limit']]
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Featured Categories du Blog'
        template = 'blog/limited_blog_category_list.html'

class PaginatedServiceListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=6, help_text="Nombre de services par page")
    categories = blocks.ListBlock(
        blocks.PageChooserBlock(target_model='service.ServiceCategoryPage'),
        required=False,
        help_text="Choisissez les catégories pour filtrer les services"
    )

    def get_context(self, value, parent_context=None):
        from service.models import ServicePage
        context = super().get_context(value, parent_context)
        request = parent_context.get('request')
        categories = value['categories']
        
        services = ServicePage.objects.live()
        if categories:
            services = services.filter(categories__in=categories)

        paginator = Paginator(services.distinct(), value['limit'])
        page_number = request.GET.get('page')
        
        try:
            paginated_services = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_services = paginator.page(1)
        except EmptyPage:
            paginated_services = paginator.page(paginator.num_pages)

        context['services'] = paginated_services
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste des Services'
        template = 'service/paginated_service_list.html'

class LimitedServiceListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de services à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les services vedettes")
    categories = blocks.ListBlock(
        blocks.PageChooserBlock(target_model='service.ServiceCategoryPage'),
        required=False,
        help_text="Choisissez les catégories pour filtrer les services"
    )

    def get_context(self, value, parent_context=None):
        from service.models import ServicePage
        context = super().get_context(value, parent_context)
        
        services = ServicePage.objects.live()
        
        if value['featured_only']:
            services = services.filter(is_featured=True)
        if value['categories']:
            services = services.filter(categories__in=value['categories'])

        context['services'] = services.distinct()[:value['limit']]
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Featured Services'
        template = 'service/limited_service_list.html'

class LimitedServiceCategoryListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de catégories de services à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les catégories vedettes")

    def get_context(self, value, parent_context=None):
        from service.models import ServiceCategoryPage
        context = super().get_context(value, parent_context)

        service_categories = ServiceCategoryPage.objects.live()
        if value['featured_only']:
            service_categories = service_categories.filter(is_featured=True)

        context['service_categories'] = service_categories.distinct()[:value['limit']]
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Featured Categories de Service'
        template = 'service/limited_service_category_list.html'

class PaginatedServiceCategoryListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=6, help_text="Nombre de catégories de services par page")

    def get_context(self, value, parent_context=None):
        from service.models import ServiceCategoryPage
        context = super().get_context(value, parent_context)

        request = parent_context.get('request')
        service_categories = ServiceCategoryPage.objects.live()

        paginator = Paginator(service_categories.distinct(), value['limit'])
        page_number = request.GET.get('page')

        try:
            paginated_service_categories = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_service_categories = paginator.page(1)
        except EmptyPage:
            paginated_service_categories = paginator.page(paginator.num_pages)

        context['service_categories'] = paginated_service_categories
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste des Catégories de Services'
        template = 'service/paginated_service_category_list.html'

class PaginatedBusinessLocalListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=6, help_text="Nombre d'entreprises par page")

    def get_context(self, value, parent_context=None):
        from businesslocal.models import BusinessLocalPage
        context = super().get_context(value, parent_context)
        request = parent_context.get('request')
        
        businesses = BusinessLocalPage.objects.live()
        paginator = Paginator(businesses.distinct(), value['limit'])
        page_number = request.GET.get('page')

        try:
            paginated_businesses = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_businesses = paginator.page(1)
        except EmptyPage:
            paginated_businesses = paginator.page(paginator.num_pages)

        context['businesses'] = paginated_businesses
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste des Entreprises'
        template = 'businesslocal/paginated_business_list.html'

class LimitedBusinessLocalListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre d'entreprises à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les entreprises vedettes")

    def get_context(self, value, parent_context=None):
        from businesslocal.models import BusinessLocalPage
        context = super().get_context(value, parent_context)
        
        businesses = BusinessLocalPage.objects.live()
        if value['featured_only']:
            businesses = businesses.filter(is_featured=True)

        context['businesses'] = businesses.distinct()[:value['limit']]
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Featured Entreprises'
        template = 'businesslocal/limited_business_list.html'

class PaginatedBusinessLocalCategoryListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=6, help_text="Nombre de catégories d'entreprises par page")

    def get_context(self, value, parent_context=None):
        from businesslocal.models import BusinessLocalCategory
        context = super().get_context(value, parent_context)
        request = parent_context.get('request')

        categories = BusinessLocalCategory.objects.live()
        paginator = Paginator(categories.distinct(), value['limit'])
        page_number = request.GET.get('page')

        try:
            paginated_categories = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_categories = paginator.page(1)
        except EmptyPage:
            paginated_categories = paginator.page(paginator.num_pages)

        context['categories'] = paginated_categories
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ol'
        label = 'Liste des Catégories d\'entreprises'
        template = 'businesslocal/paginated_business_category_list.html'

class LimitedBusinessLocalCategoryListBlock(blocks.StructBlock):
    heading = HeadingBlock(required=False, help_text="Titre facultatif pour cette section")
    paragraph = ParagraphBlock(required=False, help_text="Texte facultatif pour cette section")
    limit = blocks.IntegerBlock(default=5, help_text="Nombre de catégories à afficher")
    featured_only = blocks.BooleanBlock(required=False, help_text="Afficher uniquement les catégories vedettes")

    def get_context(self, value, parent_context=None):
        from businesslocal.models import BusinessLocalCategory
        context = super().get_context(value, parent_context)

        categories = BusinessLocalCategory.objects.live()
        if value['featured_only']:
            categories = categories.filter(is_featured=True)

        context['categories'] = categories.distinct()[:value['limit']]
        context['heading'] = value['heading']
        context['paragraph'] = value['paragraph']
        return context

    class Meta:
        icon = 'list-ul'
        label = 'Featured Catégories d\'entreprises'
        template = 'businesslocal/limited_business_category_list.html'

