from django.db import models
import uuid
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
# https://blog.mathieu-leplatre.info/django-selectrelated-manytomany.html
class Category(MPTTModel):

    #uuid pas bon pour la clarté !
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Created date")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Updated date")

    name = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name="Name")
    slug = models.SlugField(blank=False, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")

    # Alors les trees je n'en avais jamais entendu parler, une sorte de graph ou d'index j'ai l'impression
    # j'ai donc pris rendez-vous avec la notice de django-mptt !
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="children")

    class Meta:
        ordering = ["name"]
    
    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name
    

class Equipment(models.Model):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Created date")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Updated date")

    name = models.CharField(max_length=255, verbose_name="Name")
    slug = models.SlugField(blank=False, verbose_name="Slug")
    description = models.TextField(max_length=1000, blank=True, verbose_name="Description")
    quantity = models.PositiveBigIntegerField(null=False, default=0, verbose_name="Quantity")

    categories = models.ManyToManyField("Category", related_name="categories", verbose_name="categories")
    #  on_delete=models.PROTECT, 

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
