from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('api/products', views.ProductListAPIView.as_view(), name='product-list'),
]