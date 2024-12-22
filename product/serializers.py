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

    class Meta:
        model = Exchanged
        fields = '__all__'

class ExchangedStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchanged
        fields = ['status']


