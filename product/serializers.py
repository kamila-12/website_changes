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
    product_offered = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_requested = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    


    class Meta:
        model = Exchanged
        fields = ['id', 'product_offered', 'product_requested', 'status', 'date_created']
        read_only_fields = ['user_requested', 'date_created']
        
    def create(self, validated_data):
        # Автоматически задаём user_requested
        validated_data['user_requested'] = validated_data['product_requested'].owner
        return super().create(validated_data)

class ExchangedStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchanged
        fields = ['status']


