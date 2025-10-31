from rest_framework.views import APIView
from . import models, serializers
from account.models import Buyer
from market.models import Product
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status

@extend_schema(tags=["Cart"])
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get(self, request):
        user = self.request.user
        buyer = Buyer.objects.get(account=user)
        cart = models.Cart.objects.get(owner=buyer, paid=False)
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=["Cart"])
class AddCartItem(APIView):
    serializer_class = serializers.AddToCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get("product_id")
            quantity = request.data.get("quantity")

            user = self.request.user.buyer
            cart, created = models.Cart.objects.get_or_create(owner=user)
            product = Product.objects.get(id=product_id)

            cartitem, created = models.CartItem.objects.get_or_create(cart=cart, product=product, quantity=quantity)
            cartitem.save()

            serializer = serializers.CartItemSerializer(cartitem)
            return Response({"data": serializer.data, "success": "Product added to cart."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Cart"])
class UpdateCart(APIView):
    serializer_class = serializers.UpdateCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            quantity = request.data.get("quantity")
            cartitem_id = request.data.get("cartitem_id")

            user = self.request.user.buyer
            cart = models.Cart.objects.get(owner=user)
            cartitem = models.CartItem.objects.get(cart=cart, id=cartitem_id)
            cartitem.quantity = int(quantity)
            cartitem.save()
            if cartitem.quantity <= 0:
                cartitem.delete()
            serializer = serializers.CartItemSerializer(cartitem)
            return Response({"data": serializer.data, "success": "Cart Updated."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Cart"])     
class DeleteCartItem(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, cartitem_id):
        try:
            cartitem = models.CartItem.objects.get(id=cartitem_id)
            cartitem.delete()
            return Response({"success": "Product Removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Cart"])
class ProductInCart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        user = self.request.user.buyer
        cart, created = models.Cart.objects.get_or_create(owner=user)
        product = Product.objects.get(id=product_id)

        product_in_cart = models.CartItem.objects.filter(cart=cart, product=product).exists()

        return Response({'product_in_cart': product_in_cart})
