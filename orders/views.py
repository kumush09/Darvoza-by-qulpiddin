from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
# Create your views here.
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated] 
    def list(self, request):
        savat = Cart.objects.get_or_create(user=request.user)[0]
        serializer = CartSerializer(savat)
        return Response(serializer.data)

    def create(self, request):
        savat = Cart.objects.get_or_create(user=request.user)[0]
        mahsulot_id = request.data.get('product_id')
        soni = int(request.data.get('quantity', 1))
        mahsulot = CartItem.objects.filter(cart=savat, product_id=mahsulot_id).first()
        if not mahsulot:
            mahsulot = CartItem.objects.create(cart=savat, product_id=mahsulot_id, quantity=0)
        mahsulot.quantity += soni
        mahsulot.save()
        return Response({"message": "Savatga qo'shildi"})
    def destroy(self, request, pk=None):
        savat = Cart.objects.filter(user=request.user).first()
        if not savat:
            return Response({"error": "Savatingiz hali bo'sh!"}, status=404)
        mahsulot = CartItem.objects.filter(cart=savat, product_id=pk).first()
        if not mahsulot:
            return Response({"error": "Bu mahsulot savatingizda yo'q!"}, status=404)
        if mahsulot.quantity > 1:
            mahsulot.quantity -= 1
            mahsulot.save()
            return Response({"message": "Mahsulot soni 1 taga kamaytirildi."})
        else:
            mahsulot.delete()
            return Response({"message": "Mahsulot savatdan butunlay o'chirildi."})
    

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        if request.user.is_staff:
            buyurtmalar = Order.objects.all()
        else:
            buyurtmalar = Order.objects.filter(user=request.user)
            
        serializer = OrderSerializer(buyurtmalar, many=True)
        return Response(serializer.data)
    def create(self, request):
        User = get_user_model()
        aniq_foydalanuvchi = User.objects.get(id=request.user.id)
        savat = Cart.objects.filter(user=aniq_foydalanuvchi).first()
        if not savat or not savat.items.exists():
            return Response({"error": "Savatingiz bo'sh! Oldin mahsulot qo'shing."}, status=400)
        manzil = request.data.get('address')
        if not manzil:
            return Response({"error": "Manzilni (address) kiritish majburiy!"}, status=400)
        jami_summa = 0
        for element in savat.items.all():
            jami_summa += element.product.price * element.quantity
        buyurtma = Order.objects.create(
            user=aniq_foydalanuvchi,
            total_sum=jami_summa,
            address=manzil,
            status='pending'  
        )
        for element in savat.items.all():
            OrderItem.objects.create(
                order=buyurtma,
                product=element.product,
                quantity=element.quantity,
                price=element.product.price
            )
        savat.items.all().delete()
        
        return Response({
            "message": "Buyurtmangiz muvaffaqiyatli qabul qilindi!",
            "order_id": buyurtma.id,
            "total_sum": jami_summa
        }, status=201)
    