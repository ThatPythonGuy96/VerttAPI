from rest_framework import serializers
from . import models
from market.serializers import ProductSerializer, CustomPriceSerializer
from drf_spectacular.utils import extend_schema_field

class CustomDateTimeSerializer(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")

class CartItemSerializer(serializers.ModelSerializer):
    item_total = serializers.SerializerMethodField()
    product = ProductSerializer(read_only=True)
    added = CustomDateTimeSerializer()
        
    def get_item_total(self, obj):
        if obj.product.discount_price:
            price = obj.product.discount_price * obj.quantity
            return f"{price:,.2f}"
        else:
            price = obj.product.price * obj.quantity
            return f"{price:,.2f}"

    class Meta:
        model = models.CartItem
        fields = ('id', 'product', 'quantity', 'added', 'item_total')

class CartSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    created = CustomDateTimeSerializer()
    modified = CustomDateTimeSerializer()
    total = serializers.SerializerMethodField()
    cart = CartItemSerializer(read_only=True, many=True)
    num_of_items = serializers.SerializerMethodField()

    def get_owner(self, obj):
        buyer = obj.owner.account.email
        return buyer

    def get_total(self, obj):
        total_price = sum(
            [(item.product.discount_price if item.product.discount_price else item.product.price) * item.quantity 
            for item in obj.cart.all()]
        )
        return f"{total_price:,.2f}"

    def get_num_of_items(self, obj):
        num_of_items = sum([item.quantity for item in obj.cart.all()])
        return num_of_items

    class Meta:
        model = models.Cart
        fields = ('cart_id', 'owner', 'cart', 'created', 'modified', 'total', 'num_of_items')

class AddToCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    product_id = serializers.IntegerField()

class UpdateCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()