from django.contrib.auth.models import User
from rest_framework import serializers
from product_serializers import ProductSerializer
from ..models import Cart, CartItem


class CartItemSerizlizer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    item = serializers.SerializerMethodField()

    def get_item_total(self, obj):
        return obj.item_total

    class Meta:
        model = CartItem
        fields = ['cart',
                  'product',
                  'item_total',
                  'amount'
                ]
        

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerizlizer(source="items", many=True)

    def get_total(self, obj):
        return sum([item.item_total for item in obj.items.all()])

    class Meta:
        model = Cart
        fields = [
            "user",
            "items",
            "created_at",
            "total"
        ]
    