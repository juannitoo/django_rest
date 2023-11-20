from django.contrib import admin
from authentication.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]

admin.site.register(User, UserAdmin)