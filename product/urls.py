from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'exchanged', views.ExchangedViewSet, basename='exchanged')  

urlpatterns = [
    path('api/products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/', include(router.urls)),  
    path('api/user/products/', views.UserProductsAPIView.as_view(), name='user-products'),
    path('api/user/exchanges/', views.UserExchangesAPIView.as_view(), name='user-exchanges'),
]
