from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Category, Equipment

 
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
    
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