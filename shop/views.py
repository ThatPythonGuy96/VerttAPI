from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Shop"])
class ShopView(APIView):
    serializer_class = serializers.ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        seller = self.request.user.seller
        shop = models.Shop.objects.get(owner=seller)
        serializer = serializers.ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        seller = self.request.user.seller
        shop = models.Shop.objects.get(owner=seller)
        shop.delete()
        return Response({"success": "Shop Closed."}, status=status.HTTP_204_NO_CONTENT)