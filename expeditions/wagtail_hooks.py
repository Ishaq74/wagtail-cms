from wagtail import hooks
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import ShippingOption


@hooks.register("register_admin_urls")
def register_shipping_urls():
    return [
        path("admin/expeditions/update/", update_shipping_options_action, name="update_shipping_options"),
    ]


def update_shipping_options_action(request):
    options = ShippingOption.objects.all()
    for option in options:
        option.save()  # Rafraîchissement des données si nécessaire
    messages.success(request, "Toutes les options d'expédition ont été mises à jour.")
    return redirect("/admin/expeditions/")
