from rest_framework import serializers
from . import models
from account.models import Seller
from shop.models import Shop

class CustomPriceSerializer(serializers.DecimalField):
    def to_representation(self, value):
        return f"{value:,.2f}"
    
class ShopDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ('name',)

class CategoryProductSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    def get_products(self, obj):
        products = obj.product_category.all()
        return ProductSerializer(products, many=True).data

    def get_subcategories(self, obj):
        subcategories = obj.subcategory.all()
        return SubCategorySerializer(subcategories, many=True).data

    class Meta:
        model = models.Category
        fields = ('id', 'category', 'image', 'products', 'subcategories')

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('id', 'category', 'image')

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubCategory
        fields = ('id', 'subcategory')

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductImage
        fields = ("id", "product", "image")

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    shop = ShopDetailSerializer()
    price = CustomPriceSerializer(max_digits=10, decimal_places=2)
    discount_price = CustomPriceSerializer(max_digits=10, decimal_places=2)
    product_images = serializers.SerializerMethodField()

    def get_product_images(self, obj):
        images = models.ProductImage.objects.filter(product=obj)
        if images:
            return ProductImageSerializer(images, many=True).data
        return []
    
    class Meta:
        model = models.Product
        fields = ('id', 'name', 'description', 'category', 'subcategory', 'price', 'discount_price', 'quantity', 'shop', 'product_images')

class CreateProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    price = CustomPriceSerializer(max_digits=10, decimal_places=2)
    discount_price = CustomPriceSerializer(max_digits=10, decimal_places=2)

    class Meta:
        model = models.Product
        fields = ('name', 'description', 'category', 'subcategory', 'price', 'discount_price', 'quantity')
        
    def create(self, validated_data):
        account = self.context['request'].user
        seller = Seller.objects.get(account__email=account.email)
        shop_ = Shop.objects.get(owner=seller)

        product = models.Product.objects.create(
            name = validated_data['name'],
            category = validated_data['category'],
            description = validated_data['description'],
            subcategory = validated_data['subcategory'],
            price = validated_data['price'],
            discount_price = validated_data['discount_price'],
            quantity = validated_data['quantity'],
            shop = shop_
        )
        product.save()
        return product
    
class ShopProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    price = CustomPriceSerializer(max_digits=10, decimal_places=2)
    discount_price = CustomPriceSerializer(max_digits=10, decimal_places=2)

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'category', 'subcategory', 'price', 'discount_price', 'quantity')