from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from products.models import Product,Category
from . import serializers


class HomePageView(APIView):
    """
    List the products available on the home page
    fields:
    category , name , slug , is_available , image , price , description , created , updated
    """

    def get(self,request):
        categories = Category.objects.all()
        products = Product.objects.filter(is_available=True)  # Available products
        srz_products = serializers.ProductSerializer(products,many=True)
        srz_categories = serializers.CategorySerializer(categories,many=True)
        return Response({'categories':srz_categories.data,'products':srz_products.data},status=status.HTTP_200_OK)