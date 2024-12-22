from rest_framework import generics, permissions, viewsets, status
from .models import Product, Exchanged
from .serializers import ProductSerializer, ExchangedSerializer, ExchangedStatusSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ExchangedViewSet(viewsets.ModelViewSet):
    queryset = Exchanged.objects.all()
    serializer_class = ExchangedSerializer

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
    

