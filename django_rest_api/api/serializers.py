from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Category, Equipment

 
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

    def validate(self, data):
        print('validation')
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=data['name']).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Category already exists errorirrfzf')
        if len(data['slug']) == 0:
            raise serializers.ValidationError('description vide')
        return data    
class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'slug']


class EquipmentListSerializer(ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description']

class EquipmentDetailsSerializer(ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description', 'quantity', 'slug', 'categories']