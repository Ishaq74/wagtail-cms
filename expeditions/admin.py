from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import ShippingOption


class ShippingOptionViewSet(SnippetViewSet):
    model = ShippingOption
    menu_label = "Factures"
    menu_icon = "doc-full"
    list_display = ("number", "customer_name", "total_ttc", "created_at", "status")  # Assurez-vous que ces champs existent
    search_fields = ("number", "customer_name", "email")

register_snippet(ShippingOptionViewSet)