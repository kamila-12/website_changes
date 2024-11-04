from rest_framework import generics, permissions, viewsets
from .models import Product, Exchanged
from .serializers import ProductSerializer, ExchangedSerializer


class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExchangedViewSet(viewsets.ModelViewSet):
    queryset = Exchanged.objects.all()
    serializer_class = ExchangedSerializer


class UserProductsAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Доступно только аутентифицированным пользователям

    def get_queryset(self):
        # Возвращаем товары, принадлежащие текущему пользователю
        return Product.objects.filter(owner=self.request.user)
    
class UserExchangesAPIView(generics.ListAPIView):
    serializer_class = ExchangedSerializer
    permission_classes = [permissions.IsAuthenticated]  # Доступно только аутентифицированным пользователям

    def get_queryset(self):
        # Показываем обмены, где текущий пользователь либо предложил товар, либо запросил его
        return Exchanged.objects.filter(
            product_offered__owner=self.request.user
        ) | Exchanged.objects.filter(user_requested=self.request.user)
