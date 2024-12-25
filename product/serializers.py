from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Exchanged

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


class ExchangedSerializer(serializers.ModelSerializer):
    product_offered = ProductSerializer()  
    product_requested = ProductSerializer()  
    sender = serializers.SerializerMethodField()  
    receiver = serializers.SerializerMethodField()  

    class Meta:
        model = Exchanged
        fields = [
            'id',
            'product_offered',
            'product_requested',
            'status',
            'date_created',
            'sender',
            'receiver'
        ]
        read_only_fields = ['user_requested', 'date_created']
    def get_sender(self, obj):
        # Проверяем наличие владельца продукта, чтобы избежать ошибок
        return obj.product_offered.owner.username if obj.product_offered and obj.product_offered.owner else "Unknown"

    def get_receiver(self, obj):
        # Проверяем наличие user_requested
        return obj.user_requested.username if obj.user_requested else "Unknown"

    def create(self, validated_data):
        # Автоматически задаём user_requested
        validated_data['user_requested'] = validated_data['product_requested'].owner
        return super().create(validated_data)

class ExchangedStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchanged
        fields = ['status']
        


