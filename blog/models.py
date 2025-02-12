from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.images.models import Image
from streams import blocks as custom_blocks
from modelcluster.fields import ParentalManyToManyField

# BlogIndexPage - Page d'accueil du blog
class BlogIndexPage(Page):
    max_count = 1
    excerpt = models.TextField(max_length=250, blank=True, help_text='Texte affiché en haut de la page')
    content = RichTextField(blank=True)
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Image principale de la page")
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
        ('paginated_businesslocal_list', custom_blocks.PaginatedBusinessLocalListBlock()),
        ('limited_businesslocal_list', custom_blocks.LimitedBusinessLocalListBlock()),
        ('paginated_businesslocal_category_list', custom_blocks.PaginatedBusinessLocalCategoryListBlock()),
        ('limited_businesslocal_category_list', custom_blocks.LimitedBusinessLocalCategoryListBlock()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('excerpt'),
        FieldPanel('content'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]

    page_description = "Page d'accueil du Blog"

    subpage_types = ['BlogCategoryPage']

    def get_context(self, request):
        context = super().get_context(request)
        blogcategories = self.get_children().live().type(BlogCategoryPage).order_by('first_published_at')
        paginator = Paginator(blogcategories, 12)
        page = request.GET.get('page')
        try:
            categories_paginated = paginator.page(page)
        except PageNotAnInteger:
            categories_paginated = paginator.page(1)
        except EmptyPage:
            categories_paginated = paginator.page(paginator.num_pages)
            
        featured_articles = BlogPage.objects.live().filter(is_featured=True).order_by('-date')[:6]

        context['blogcategories'] = categories_paginated
        context['pagination'] = categories_paginated
        context['featured_articles'] = featured_articles
        return context

    class Meta:
        verbose_name = "Page d'accueil du Blog"

class BlogCategoryPage(Page):
    excerpt = models.TextField(max_length=250, blank=True, help_text='Texte affiché en haut de la page')
    content = RichTextField(blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+',
        help_text="Image principale de la page"
    )
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
        ('paginated_businesslocal_list', custom_blocks.PaginatedBusinessLocalListBlock()),
        ('limited_businesslocal_list', custom_blocks.LimitedBusinessLocalListBlock()),
        ('paginated_businesslocal_category_list', custom_blocks.PaginatedBusinessLocalCategoryListBlock()),
        ('limited_businesslocal_category_list', custom_blocks.LimitedBusinessLocalCategoryListBlock()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('excerpt'),
        FieldPanel('content'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]

    page_description = "Catégorie pour organiser les articles de blog"
    subpage_types = ['BlogPage', 'BlogCategoryPage']
    parent_page_types = ['BlogIndexPage', 'BlogCategoryPage']

    def get_context(self, request):
        context = super().get_context(request)
        blogcategories = self.get_children().live().type(BlogCategoryPage).order_by('-first_published_at')
        blogpages = self.get_children().live().type(BlogPage).order_by('-first_published_at')

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
        context['pagination'] = blogpages_paginated
        context['related_categories'] = self.get_siblings()
        return context

    class Meta:
        verbose_name = "Catégorie de Blog"
        verbose_name_plural = "Catégories de Blogs"


    page_description = "Catégorie pour organiser les articles de blog"

    subpage_types = ['BlogPage', 'BlogCategoryPage']
    parent_page_types = ['BlogIndexPage', 'BlogCategoryPage']

    def get_context(self, request):
        context = super().get_context(request)
        blogcategories = self.get_children().live().type(BlogCategoryPage).order_by('-first_published_at')
        blogpages = self.get_children().live().type(BlogPage).order_by('-first_published_at')
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
        context['pagination'] = blogpages_paginated
        return context

    class Meta:
        verbose_name = "Catégorie de Blog"
        verbose_name_plural = "Catégories de Blogs"

# BlogPage - Article de blog
class BlogPage(Page):
    categories = ParentalManyToManyField('BlogCategoryPage', blank=True)
    is_featured = models.BooleanField(default=False, help_text="Marquer cet article comme en vedette")
    date = models.DateField("Date de publication")
    excerpt = models.TextField(max_length=250, blank=True, help_text='Texte affiché en haut de la page')
    content = RichTextField(blank=True)
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Image principale de la page")
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
        ('paginated_businesslocal_list', custom_blocks.PaginatedBusinessLocalListBlock()),
        ('limited_businesslocal_list', custom_blocks.LimitedBusinessLocalListBlock()),
        ('paginated_businesslocal_category_list', custom_blocks.PaginatedBusinessLocalCategoryListBlock()),
        ('limited_businesslocal_category_list', custom_blocks.LimitedBusinessLocalCategoryListBlock()),
    ], null=True, blank=True, use_json_field=True)


    content_panels = Page.content_panels + [
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('is_featured'),
        FieldPanel('date'),
        FieldPanel('excerpt'),
        FieldPanel('content'),
        FieldPanel('featured_image'),
        FieldPanel('body'),
    ]

    subpage_types = []
    parent_page_types = ['BlogCategoryPage']

    def get_siblings(self):
        siblings = BlogPage.objects.live().sibling_of(self).exclude(id=self.id)[:3]
        return siblings

    def get_context(self, request):
        context = super().get_context(request)
        context['related_articles'] = self.get_siblings()
        return context

    class Meta:
        verbose_name = "Article de Blog"
