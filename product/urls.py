from django.urls import include, path
from rest_framework import routers
from . import views
from .views import UpdateExchangeStatusAPIView, ProfileView, ExchangeViewSet
from django.conf.urls.static import static
from django.conf import settings
router = routers.DefaultRouter()
router.register(r'exchanges', ExchangeViewSet)

urlpatterns = [
    path('api/user/products/', views.UserProductsAPIView.as_view(), name='user-products'),
    path('api/products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/user/exchanges/', views.UserExchangesAPIView.as_view(), name='user-exchanges'),
    path('api/', include(router.urls)),  # Подключение ViewSet
    path('api/exchange/<int:pk>/update-status/', UpdateExchangeStatusAPIView.as_view(), name='update-exchange-status'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    ]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
