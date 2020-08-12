from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework.serializers import CharField

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 
        
    categoryName = CharField(source='category.name', default='')       