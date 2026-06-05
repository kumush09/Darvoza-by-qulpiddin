from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserProfileSerializer
from .models import *
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class ShaxsAccessTokenView(APIView):
    def post(self, request):
        name = request.data.get('name')
        print(request.data)
        obj = Shaxs.objects.get(name=name)
        token = AccessToken.for_user(obj)
        return Response({'token': str(token)})
    
class ShaxsRefreshTokenView(APIView):
    def post(self, request):
        name = request.data.get('name')
        obj = Shaxs.objects.get(name=name)
        
        refresh = RefreshToken.for_user(obj)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })
    

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Muallafaqiyatli ro'yxatdan o'tdingiz!"})
        return Response(serializer.errors, status=400)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profil yangilandi!"})
        return Response(serializer.errors, status=400)