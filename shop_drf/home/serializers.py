from rest_framework import serializers
from products.models import Product,Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_sub_category(self,obj):
        if obj.sub_category:
            return obj.sub_category.name
        return None
