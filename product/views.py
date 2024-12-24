from rest_framework import generics, permissions, viewsets, status
from .models import Product, Exchanged
from .serializers import ProductSerializer, ExchangedSerializer, ExchangedStatusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UpdateExchangeStatusAPIView(generics.UpdateAPIView):
    queryset = Exchanged.objects.all()
    serializer_class = ExchangedStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ограничиваем доступ только к обменам, где пользователь имеет право менять статус
        return Exchanged.objects.filter(
            product_requested__owner=self.request.user
        )
    def get(self, request, *args, **kwargs):
        exchange = self.get_object()
        serializer = self.get_serializer(exchange)
        return Response(serializer.data)


class UserProductsAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        # Сохраняем продукт с владельцем текущим пользователем
        serializer.save(owner=self.request.user)


class UserExchangesAPIView(generics.ListAPIView):
    serializer_class = ExchangedSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        return Exchanged.objects.filter(
            product_offered__owner=self.request.user
        ) | Exchanged.objects.filter(user_requested=self.request.user)


# view для обмена
class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchanged.objects.all()
    serializer_class = ExchangedSerializer

    @action(detail=False, methods=['post'])
    def create_exchange(self, request):
        product_offered = request.data.get('product_offered')
        product_requested = request.data.get('product_requested')

        # Проверяем существование продуктов
        try:
            product_offered_obj = Product.objects.get(id=product_offered)
            product_requested_obj = Product.objects.get(id=product_requested)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Создаём обмен
        exchange = Exchanged.objects.create(
            product_offered=product_offered_obj,
            product_requested=product_requested_obj,
            status='pending'
        )

        return Response({'id': exchange.id, 'status': 'exchange created'}, status=status.HTTP_201_CREATED)


