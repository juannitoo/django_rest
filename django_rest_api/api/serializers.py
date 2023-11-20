from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Category, Equipment

 
class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category list serializer
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class CategoryDetailsSerializer(serializers.ModelSerializer):
    """
    Category details serializer
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'slug']
        depth = 1

    # https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
    # je laisse les validations du modèle
    # def validate_description(self, value):
    #     if len(value) == 0:
    #         raise serializers.ValidationError('description vide')
    #     return value
    # 
    # def validate(self, data):
    #   return data    


class EquipmentListSerializer(ModelSerializer):
    """
    Equipement list serializer
    """
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description']

class EquipmentDetailsSerializer(ModelSerializer):
    """
    Equipement details serializer
    """
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description', 'quantity', 'slug', 'categories']
        depth = 1