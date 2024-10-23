from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer

# API для списка продуктов
class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Аутентификация только для создания

# API для детального просмотра и редактирования продукта
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Аутентификация для редактирования и удаления
