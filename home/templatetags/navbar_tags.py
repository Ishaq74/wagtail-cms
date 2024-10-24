from django import template
from wagtail.models import Page
from home.models import HomePage
from flex.models import FlexPage
from blog.models import BlogIndexPage, BlogCategoryPage

register = template.Library()

@register.simple_tag
def get_navbar_pages():
    # Récupérer la page d'accueil et les pages flex (A propos, Contact)
    home_and_flex_pages = Page.objects.live().public().in_menu().type(HomePage, FlexPage)
    
    # Récupérer le BlogIndexPage indépendamment du contexte de la page actuelle
    blog_index = BlogIndexPage.objects.live().public().in_menu().first()

    # Si une page BlogIndex existe, on récupère les catégories de blog associées (2 niveaux max)
    if blog_index:
        blog_categories = Page.objects.live().public().in_menu().descendant_of(blog_index).type(BlogCategoryPage)
    else:
        blog_categories = []

    return {
        'home_and_flex_pages': home_and_flex_pages,
        'blog_index': blog_index,
        'blog_categories': blog_categories
    }
