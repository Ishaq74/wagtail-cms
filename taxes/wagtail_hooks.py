from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.models import Site
from django.shortcuts import redirect
from django.contrib import messages
from .models import Tax


@hooks.register("construct_main_menu")
def add_taxes_to_menu(request, menu_items):
    menu_items.append(
        MenuItem("Taxes", "/admin/snippets/taxes/tax/", icon_name="form")
    )
