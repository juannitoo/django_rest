from django.db import models
import uuid
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("created date"))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))
    name = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name=_("name"))
    slug = models.SlugField(blank=False, verbose_name=_("slug"))
    description = models.TextField(blank=True, verbose_name=_("description"))

    # Alors les trees je n'en avais jamais entendu parler, une sorte de graph ou d'index j'ai l'impression
    # qui sert à économiser le moteur sql et à gagner en temps de réponse.
    # j'ai donc pris rendez-vous avec la notice de django-mptt !
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children", verbose_name=_("parent"))

    class Meta:
        ordering = ["name"]
        verbose_name = _('category')
        verbose_name_plural = _('categories')
    
    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name
    

class Equipment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("created date"))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.SlugField(blank=False, verbose_name=_("slug"))
    description = models.TextField(max_length=1000, blank=True, verbose_name=_("description"))
    quantity = models.PositiveBigIntegerField(null=False, default=0, verbose_name=_("quantity"))
    categories = models.ManyToManyField("Category", related_name="categories", verbose_name=_("categories"))

    class Meta:
        ordering = ["name"]
        verbose_name = _('equipment')
        verbose_name_plural = _('equipments')

    def __str__(self):
        return self.name
    
