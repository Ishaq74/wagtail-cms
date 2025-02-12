
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Adresse email')
    first_name = forms.CharField(required=False, label='Prénom')
    last_name = forms.CharField(required=False, label='Nom de famille')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    password = None  # On n'affiche pas le champ mot de passe

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'phone_number',
            'address_line1', 'address_line2', 'city', 'postal_code', 'country',
            'profile_picture'
        )
