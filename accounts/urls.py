# accounts/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('inscription/', views.register, name='register'),
    path('activation/<uidb64>/<token>/', views.activate, name='activate'),
    path('connexion/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    path('mot-de-passe-oublie/envoye/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reinitialisation-mot-de-passe/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reinitialisation-mot-de-passe/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('profil/editer/', views.edit_profile, name='edit_profile'),
    path('supprimer-compte/', views.delete_account, name='delete_account'),
    # Ajoutez les URLs pour la gestion des adresses multiples si nécessaire
]
