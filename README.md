# Test à réaliser

### Setup

git clone  
python -m venv env ==> dans le dossier cloné pour créer un environnement virtuel pour le projet  
source env/bin/activate ==> pour activer l'environnement depuis la racine du projet.  
pip install -r requirements.txt ==> pour installer les dépendances nécessaires.  
cd django_rest_api/  
python manage.py migrate ==> pour initialiser la base de données  
renseigner le superUser de la BDD dans api/management/commands/init_db.py  
python manage.py init_db ==> pour peupler la base de données

### A savoir

##### Back

C'est ma première utilisation de Django-rest.  
Je n'ai jamais fait de tests unitaires en Python.  
Je ne connaissais pas les Trees du modèle.  
Les traductions des champs du modèle ne fonctionnent pas tous dans l'admin comme "quantity" qui n'est pas traduit alors que "name" est bien traduit.  
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

Il n'y en a pas, je ne connais rien de react, et comme j'ai du apprendre django-rest (vite vite), j'ai préféré me focalisé là dessus.
