from django.urls import include, path, re_path
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import UpdateExchangeStatusAPIView

router = routers.DefaultRouter()
router.register('exchanged', views.ExchangedViewSet, basename='exchanged')  

urlpatterns = [
    path('', views.UserProductsAPIView.as_view(), name='user-products'),
    path('api/products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/', include(router.urls)),  
    path('api/user/exchanges/', views.UserExchangesAPIView.as_view(), name='user-exchanges'),
    path('api/exchange/request/', views.UserExchangedRequestAPIView.as_view(), name='exchange-request'),
    path('api/exchange/<int:pk>/update-status/', UpdateExchangeStatusAPIView.as_view(), name='update-exchange-status'),

    path('api/v1/auth/', include('djoser.urls')),         
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    ]

