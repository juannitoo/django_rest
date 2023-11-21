from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# https://openclassrooms.com/fr/courses/7192426-allez-plus-loin-avec-le-framework-django/7386368-personnalisez-le-modele-utilisateur
# ces champs sont induit via l'hériatge de abstractuser
# username  (nom d’utilisateur) — utilisé pour se connecter
# first_name  (prénom)
# last_name  (nom de famille)
# email
# password  (mot de passe) — les mots de passe sont stockés après hachage dans la base de données. Ne sauvegardez jamais de mots de passe en clair.
# is_staff  (est un membre du personnel) — un booléen ; détermine si un utilisateur peut se connecter au site administrateur Django.
# is_active  (est actif) — un booléen ; on considère que c’est une meilleure pratique avec Django de signaler que des utilisateurs sont inactifs en réglant cet attribut sur  False  plutôt que de les supprimer.
# is_superuser  (est un superutilisateur) — un booléen ; les superusers, ou superutilisateurs, obtiennent automatiquement toutes les permissions, telles que l’accès au site administrateur.

class User(AbstractUser):
    pass

# class Token(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", verbose_name=_("user"))
#     refresh_token = models.CharField(max_length=255, null=False, blank=False, verbose_name=_("refresh-token"))