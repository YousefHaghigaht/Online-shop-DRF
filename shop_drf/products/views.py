from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from django.shortcuts import get_object_or_404
from home.serializers import ProductSerializer
from rest_framework import status
from . import tasks, serializers
from rest_framework.permissions import IsAdminUser


class ProductDetailView(APIView):
    """
    Show a product
        fields:
    category , name , slug , is_available , image , price , description , created , updated
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['post_id'], slug=kwargs['post_slug'])
        srz_product = ProductSerializer(product)
        return Response(data={'product': srz_product.data}, status=status.HTTP_200_OK)


class BucketListObjectsView(APIView):
    """P:"{)9 532       Q4590
    Display a list of object    c b7s in storage

    Using the field serializer of their content objects
    We show

    fields:
    Key , LastModified , Size
    """
    permission_classes = [IsAdminUser]
    def get(self, request):
        try:
            result = tasks.list_objects_task()
            srz_data = serializers.BucketListObjectsSerializer(result, many=True)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BucketDeleteObjectView(APIView):

    """
    Delete it by passing the "key" value of the desired string.
    This view works with celery.
    """
    permission_classes = [IsAdminUser]

    def delete(self, request, key):
        result = tasks.delete_object_task.delay(key)
        if result:
            return Response({'message': 'Deleted object'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'The desired object does not exist'}, status=status.HTTP_404_NOT_FOUND)


class BucketDownloadObjectView(APIView):
    """
    Download the desired string by sending the "key" value.
    This view works with celery.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, key):
        result = tasks.download_object_task.delay(key)
        if result:
            return Response({'message':'Start downloading...'})
        else:
            return Response({'message':'The desired object does not exist'},status=status.HTTP_404_NOT_FOUND)
