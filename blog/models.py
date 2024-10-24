from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.images.models import Image

# BlogIndexPage - Page d'accueil du blog
class BlogIndexPage(Page):
    max_count = 1
    subtitle = models.CharField(max_length=255, default="Recent Posts")
    summary = models.TextField(max_length=250, blank=True, help_text='Texte affiché en haut de la page et en extrait')
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('summary'),
        FieldPanel('body'),
    ]

    page_description = "Page d'accueil du Blog"

    subpage_types = ['BlogCategoryPage']

    # Pagination pour les catégories de blog, 3 catégories par page
    def get_context(self, request):
        context = super().get_context(request)
        blogcategories = self.get_children().live().type(BlogCategoryPage).order_by('first_published_at')

        # Pagination - 3 catégories par page
        paginator = Paginator(blogcategories, 3)
        page = request.GET.get('page')

        try:
            categories_paginated = paginator.page(page)
        except PageNotAnInteger:
            categories_paginated = paginator.page(1)
        except EmptyPage:
            categories_paginated = paginator.page(paginator.num_pages)

        context['blogcategories'] = categories_paginated
        context['pagination'] = categories_paginated  # Pour la pagination dans le template
        return context


# BlogCategoryPage - Page de catégorie de blog
class BlogCategoryPage(Page):
    summary = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    is_featured = models.BooleanField(default=False, help_text="Marquer cette catégorie comme mise en avant.")
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('body'),
        FieldPanel('is_featured'),
        FieldPanel('featured_image'),
    ]

    page_description = "Catégorie pour organiser les articles de blog"

    subpage_types = ['BlogPage', 'BlogCategoryPage']
    parent_page_types = ['BlogIndexPage', 'BlogCategoryPage']

    # Pagination pour les articles de la catégorie, 5 articles par page
    def get_context(self, request):
        context = super().get_context(request)
        blogcategories = self.get_children().live().type(BlogCategoryPage).order_by('-first_published_at')
        blogpages = self.get_children().live().type(BlogPage).order_by('-first_published_at')

        # Pagination des articles - 5 articles par page
        paginator = Paginator(blogpages, 3)
        page = request.GET.get('page')

        try:
            blogpages_paginated = paginator.page(page)
        except PageNotAnInteger:
            blogpages_paginated = paginator.page(1)
        except EmptyPage:
            blogpages_paginated = paginator.page(paginator.num_pages)

        context['blogcategories'] = blogcategories
        context['blogpages'] = blogpages_paginated
        context['pagination'] = blogpages_paginated  # Pagination pour les articles
        return context


# BlogPage - Article de blog
class BlogPage(Page):
    date = models.DateField("Date de publication")
    summary = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    is_featured = models.BooleanField(default=False, help_text="Marquer cet article comme mis en avant.")
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('summary'),
        FieldPanel('body'),
        FieldPanel('is_featured'),
        FieldPanel('featured_image'),
    ]

    subpage_types = []  # Un article ne peut pas avoir d'enfants
    parent_page_types = ['BlogCategoryPage']
    # Afficher les articles "siblings" (liés) dans la même catégorie
    def get_siblings(self):
        # Obtenons tous les articles du parent (catégorie) et excluons l'article actuel
        siblings = BlogPage.objects.live().sibling_of(self).exclude(id=self.id)[:3]
        return siblings

    def get_context(self, request):
        context = super().get_context(request)
        # Ajouter les articles liés (siblings) dans le contexte
        context['related_articles'] = self.get_siblings()
        return context
