# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

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
    profile_picture = models.ImageField('Photo de profil', upload_to='profile_pics/', blank=True, null=True)

    # Les champs is_active, is_staff, date_joined, username et password sont hérités de AbstractUser

    def __str__(self):
        return self.username
