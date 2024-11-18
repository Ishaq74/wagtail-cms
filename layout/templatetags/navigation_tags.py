from django import template
from layout.models import NavigationMenu

register = template.Library()


@register.simple_tag
def get_menu_items(menu_title):
    """
    Récupère les éléments d’un menu par son titre.
    """
    try:
        menu = NavigationMenu.objects.get(title=menu_title)
        return menu.items.filter(parent__isnull=True).order_by('sort_order')
    except NavigationMenu.DoesNotExist:
        return []
