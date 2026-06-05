from rest_framework import serializers
from .models import *
from products.serializers import *

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = '__all__'
    def get_total_price(self, obj):
        return obj.product.price * obj.quantity
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields ='__all__'
    def get_final_price(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return total

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total_sum', 'status']


