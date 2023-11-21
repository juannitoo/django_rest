# Test à réaliser

### Setup

1. git clone git@github.com:juannitoo/django_rest.git
2. python -m venv env ==> dans le dossier cloné pour créer un environnement virtuel pour le projet
3. source env/bin/activate ==> pour activer l'environnement depuis la racine du projet.
4. pip install -r requirements.txt ==> pour installer les dépendances nécessaires.
5. cd django_rest_api/
6. python manage.py migrate ==> pour initialiser la base de données
7. renseigner le superUser de la BDD dans api/management/commands/init_db.py
8. python manage.py init_db ==> pour peupler la base de données

### A savoir

##### Back

C'est ma première utilisation de Django-rest.  
Je n'ai jamais fait de tests unitaires en Python donc ceux sont mes premiers et ce ne fût pas simple !  
Ca me semble étonnant de ne pas avoir à stocker le refreshtoken dans la base, mais comme mon access token se rafraichit, je laisse tel quel : TokenRefreshView.as_view() de simpleJWT  
Je ne connaissais pas les Trees du modèle.  
Patch sur equipment.categories ne fontionne pas alors que sur equipment.name oui. Je ne comprends pas.  
Les traductions des champs du modèle ne fonctionnent pas toutes dans l'admin comme "quantity" qui n'est pas traduit alors que "name" est bien traduit. Ca non plus je ne comprends pas !  
[https://docs.djangoproject.com/fr/3.2/topics/i18n/translation/](https://docs.djangoproject.com/fr/3.2/topics/i18n/translation/)
J'ai pourtant mis en place ce que j'ai pu trouver dans la notice.

```
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _    *** ICI

class MyThing(models.Model):
    kind = models.ForeignKey(
        ThingKind,
        on_delete=models.CASCADE,
        related_name='kinds',
        verbose_name=_('kind'),   *** ICI
    )

    @admin.display(description=_('Is it a mouse?'))
    def is_mouse(self):
        return self.kind.type == MOUSE_TYPE
```

##### Front

Il n'y en a pas, je ne connais rien de react, et comme j'ai dû apprendre django-rest (vite, trop vite), j'ai préféré me focaliser là dessus pour la suite de mes aventures. Il manquerait au moins django-cors pour le cross-origin j'imagine.
