from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category
from .serializers import *


class ProductPagination(PageNumberPagination):
    page_size =2

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    pagination_class = ProductPagination
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer 
        return ProductDetailSerializer  
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]         
        return [IsAdminUser()]          


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]