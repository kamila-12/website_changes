from rest_framework import generics, permissions, viewsets
from .models import Product, Exchanged
from .serializers import ProductSerializer, ExchangedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

class UserExchangedRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        product_offered_id = request.data.get("product_offered")
        product_requested_id = request.data.get("product_requested")
        
        try:
            product_offered = Product.objects.get(id=product_offered_id, owner=request.user)
            product_requested = Product.objects.get(id = product_requested_id)
        except Product.DoesNotExist:
            return Response({"error: " "The product was not found or you are not owner"}, status=status.HTTP_404_NOT_FOUND)
        
        exchange = Exchanged.objects.create(
            product_offered = product_offered,
            product_requested = product_requested,
            user_requested = product_requested.owner,
            
        )
        serializer = ExchangedSerializer(exchange)
        return Response(serializer.data, status=status.HTTP_201_CREATED)