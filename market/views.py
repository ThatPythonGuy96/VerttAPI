from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from cart.models import Cart, CartItem
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Market"])
class CategoriesView(APIView):
    serializer_class = serializers.CategorySerializer

    def get(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Market"])
class CategoryView(APIView):
    serializer_class = serializers.CategorySerializer

    def get(self, request, id):
        category = models.Category.objects.get(id=id)
        serializer = serializers.CategoryProductSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(tags=["Market"])
class SubcategoriesView(APIView):
    serializer_class = serializers.SubCategorySerializer

    def get(self, request):
        subcategories = models.SubCategory.objects.all()
        serializer = serializers.SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Market"])
class SubcategoryView(APIView):
    serializer_class = serializers.SubCategorySerializer

    def get(self, request, id):
        subcategory = models.SubCategory.objects.get(id=id)
        serializer = serializers.SubCategorySerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@extend_schema(tags=["Market"])
class ProductsView(APIView):
    serializer_class = serializers.ProductSerializer

    def get(self, request):
        products = models.Product.objects.all().order_by('-rating')
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Market"])
class ProductsOrderByView(APIView):
    serializer_class = serializers.ProductSerializer

    def get(self, request, order):
        products = models.Product.objects.all().order_by(order)
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Market"])
class ProductView(APIView):
    serializer_class = serializers.ProductSerializer

    def get(self, request, id):
        product = models.Product.objects.get(id=id)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Market"])
class CreateProductView(APIView):
    serializer_class = serializers.CreateProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = serializers.CreateProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)