from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import TaxProduct, TaxUser, TaxMatrice


# Enregistrer les snippets pour TaxProduct, TaxUser, et TaxMatrice
class TaxProductViewSet(SnippetViewSet):
    model = TaxProduct
    menu_label = "Taxe produit"
    menu_icon = "table"
    list_display = ("tax_name",)
    search_fields = ("tax_name",)

register_snippet(TaxProductViewSet)


class TaxUserViewSet(SnippetViewSet):
    model = TaxUser
    menu_label = "Taxe utilisateur"
    menu_icon = "table"
    list_display = ("tax_name",)
    search_fields = ("tax_name",)

register_snippet(TaxUserViewSet)


class TaxMatriceViewSet(SnippetViewSet):
    model = TaxMatrice
    menu_label = "Matrice fiscale"
    menu_icon = "table"
    list_display = ("tax_product", "tax_user", "tax_rate", "tax_account", "is_active")
    search_fields = ("tax_product__tax_name", "tax_user__tax_name", "tax_rate", "tax_account")
    list_filter = ("is_active",)

register_snippet(TaxMatriceViewSet)
