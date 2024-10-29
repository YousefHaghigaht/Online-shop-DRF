from rest_framework import serializers


class BucketListObjectsSerializer(serializers.Serializer):
    key = serializers.CharField(source='Key')
    last_modified = serializers.DateTimeField(source='LastModified')
    size = serializers.IntegerField(source='Size')