from rest_framework import serializers
from products.models import Product
from .models import Order, OrderItem, Coupon
from accounts.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_id = serializers.IntegerField()
    product_slug = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'email', 'full_name')


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    paid = serializers.BooleanField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    discount = serializers.IntegerField()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class PaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    description = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(max_length=11, required=False)


class CouponSerializer(serializers.Serializer):
    code = serializers.CharField()


class CouponPerfectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
