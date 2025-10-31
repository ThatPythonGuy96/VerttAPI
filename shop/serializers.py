from rest_framework import serializers
from . import models
from market.models import Product
from market.serializers import ShopProductSerializer
# from account.serializers import SellerSerializer
from drf_spectacular.utils import extend_schema_field

class ShopSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    # owner = SellerSerializer()

    @extend_schema_field(field=str)
    def get_products(self, obj):
        products = Product.objects.filter(shop=obj)
        return ShopProductSerializer(products, many=True).data

    class Meta:
        model = models.Shop
        fields = ('id', 'name', 'products', 'owner')

