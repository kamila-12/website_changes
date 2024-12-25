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
        # Возвращает имя владельца предложенного продукта
        return obj.product_offered.owner.username

    def get_receiver(self, obj):
        # Возвращает имя пользователя, который запросил обмен
        return obj.user_requested.username

    def create(self, validated_data):
        # Автоматически задаём user_requested
        validated_data['user_requested'] = validated_data['product_requested'].owner
        return super().create(validated_data)

class ExchangedStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchanged
        fields = ['status']
        


