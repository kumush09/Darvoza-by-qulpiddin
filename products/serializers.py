from rest_framework import serializers
from .models import *

class ProductImageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ProductImage
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True) 
    class Meta:
        model = Product
        fields = '__all__'