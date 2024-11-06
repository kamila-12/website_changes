from rest_framework import generics, permissions, viewsets
from .models import Product, Exchanged
from .serializers import ProductSerializer, ExchangedSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExchangedViewSet(viewsets.ModelViewSet):
    queryset = Exchanged.objects.all()
    serializer_class = ExchangedSerializer


class UserProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)


class UserExchangesAPIView(generics.ListAPIView):
    serializer_class = ExchangedSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Exchanged.objects.filter(
            product_offered__owner=self.request.user
        ) | Exchanged.objects.filter(user_requested=self.request.user)

