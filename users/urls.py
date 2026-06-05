from django.urls import path,re_path,include
from .views import *
from products.views import *
from orders.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')
router.register('cart', CartViewSet, basename='cart'),
router.register('orders', OrderViewSet, basename='order'),

schema_view = get_schema_view(
    openapi.Info(
        title="Darvoza API",
        default_version="v1",
        description="Bu API hujjatlari Swagger va Redoc orqali ko'rsatiladi",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns=[
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('token/',TokenObtainPairView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('shaxs/token/',ShaxsAccessTokenView.as_view()),
    path('shaxs/token/refresh/',ShaxsRefreshTokenView.as_view()),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]