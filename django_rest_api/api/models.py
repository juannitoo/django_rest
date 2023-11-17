from django.db import models
import uuid
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
# class Category(models.Model):
class Category(MPTTModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Created date")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Updated date")

    name = models.CharField(max_length=255, verbose_name="Name", null=False, unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    slug = models.SlugField(default="", null=False, verbose_name="Slug")

    # Alors les trees je n'en avais jamais entendu parler, une sorte de graph ou d'index j'ai l'impression
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    #models.PROTECT ?

    class Meta:
        ordering = ["name"]
    
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
    

class Equipment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Created date")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Updated date")

    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(max_length=1000,blank=True, verbose_name="Description")
    quantity = models.PositiveBigIntegerField(null=False, default=0, verbose_name="Quantity")
    slug = models.SlugField(default="", null=False, verbose_name="Slug")

    categories = models.ManyToManyField('Category', related_name='categories')
    # on_delete à gérér

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
