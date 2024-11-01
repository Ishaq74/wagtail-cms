# navbar_tags.py

from django import template
from wagtail.models import Page
from home.models import HomePage
from flex.models import FlexPage
from blog.models import BlogIndexPage, BlogCategoryPage
from service.models import ServiceCategoryPage
from product.models import ProductCategory

register = template.Library()

@register.simple_tag
def get_navbar_pages():
    # Récupérer la page d'accueil et les pages flex
    home_and_flex_pages = Page.objects.live().public().in_menu().type(HomePage, FlexPage)

    # Récupérer le BlogIndexPage
    blog_index = BlogIndexPage.objects.live().public().in_menu().first()

    # Récupérer les catégories de blog (2 niveaux max)
    if blog_index:
        blog_categories = blog_index.get_children().live().public().in_menu().type(BlogCategoryPage)
    else:
        blog_categories = []

    # Récupérer les catégories de services
    service_categories = ServiceCategoryPage.objects.live().public().in_menu()

    # Récupérer les catégories de produits
    product_categories = ProductCategory.objects.live().public().in_menu()

    return {
        'home_and_flex_pages': home_and_flex_pages,
        'blog_index': blog_index,
        'blog_categories': blog_categories,
        'service_categories': service_categories,
        'product_categories': product_categories,
    }
