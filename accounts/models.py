# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from taxes.models import TaxUser
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

class CustomUser(AbstractUser):
    email = models.EmailField('Adresse email', unique=True)
    first_name = models.CharField('Prénom', max_length=30, blank=True)
    last_name = models.CharField('Nom de famille', max_length=150, blank=True)
    phone_number = models.CharField('Numéro de téléphone', max_length=15, blank=True)
    address_line1 = models.CharField('Adresse ligne 1', max_length=255, blank=True)
    address_line2 = models.CharField('Adresse ligne 2', max_length=255, blank=True)
    city = models.CharField('Ville', max_length=100, blank=True)
    postal_code = models.CharField('Code postal', max_length=20, blank=True)
    country = models.CharField('Pays', max_length=100, blank=True)
    tax_user = models.ForeignKey('taxes.TaxUser', null=True, blank=True, on_delete=models.SET_NULL)
    profile_picture = models.ImageField('Photo de profil', upload_to='profile_pics/', blank=True, null=True)

    # Les champs is_active, is_staff, date_joined, username et password sont hérités de AbstractUser

    def __str__(self):
        return self.username

# Définition d'un SnippetViewSet personnalisé pour CustomUser
class CustomUserViewSet(SnippetViewSet):
    model = CustomUser
    menu_label = "Utilisateurs"
    menu_icon = "user"  # Icône de menu
    add_to_admin_menu = True
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'postal_code', 'country']
    list_filter = ['city', 'country']
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'postal_code', 'country']

# Enregistrement du snippet avec le viewset personnalisé
register_snippet(CustomUserViewSet)