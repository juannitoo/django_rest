from django.contrib import admin
from api.models import Category, Equipment

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description','slug','parent')

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name','description','quantity','slug')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Equipment, EquipmentAdmin)
