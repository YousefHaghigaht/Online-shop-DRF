from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .cart import Cart
from .serializers import CartSerializer,ProductSerializer,OrderSerializer,OrderItemSerializer,PaymentSerializer,CouponSerializer
from .models import Product,Order,OrderItem,Coupon
from django.conf import settings
import requests
from django.shortcuts import get_object_or_404
from datetime import datetime
import pytz


class CartView(APIView):
    """
     View for managing the user's shopping cart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
          GET method to retrieve the contents of the user's shopping cart.

          param request: HTTP request object
          return: JSON response containing cart information
        """

        cart = Cart(request)
        cart_items = []
        total_quantity = 0
        total_price = 0

        # Loop through each item in the shopping cart
        for item in cart:
            product = item['product']
            quantity = item['quantity']
            price = product.price
            total_item_price = price * quantity

            cart_items.append({
                'product_name': product.name,
                'product_id':product.id,
                'product_slug':product.slug,
                'quantity': quantity,
                'price': price,
                'total_price': total_item_price,
            })

            total_quantity += quantity
            total_price += total_item_price

        cart_data = {
            'items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }

        srz_data = CartSerializer(data=cart_data)
        srz_data.is_valid(raise_exception=True)

        return Response(data=srz_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(id=product_id)
            cart = Cart(request)
            cart.add(int(quantity), product)
            return Response({'message': 'product added to cart'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
            cart = Cart(request)
            cart.remove(product)
            return Response({'message':'Object deleted.'},status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({'error':'Product not found'},status=status.HTTP_404_NOT_FOUND)


class OrderCreate(APIView):
    """
    Create Order Model

    After creating the order model, the shopping cart is deleted.

    fields:
        'user' , paid , created , updated , discount
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order,products=item['product'],price=item['price'],quantity=item['quantity'])
        cart.delete()
        srz_order = OrderSerializer(instance=order)
        return Response(srz_order.data,status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    """
    Display the order details and apply the coupon code in the post method based on the field body:
    {'code':'your code'}
    """

    def setup(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order,id=kwargs['order_id'])
        return super().setup(request,*args,**kwargs)

    # Display the details of an order with this method
    def get(self, request , *args , **kwargs):
        srz_order = OrderSerializer(instance=self.order)
        return Response({'order':srz_order.data,'total_price':self.order.get_total_price()},status=status.HTTP_200_OK)

    # By sending the value of the code, the discount code is validated and applied.
    def post(self , request, *args , **kwargs):
        data = CouponSerializer(data=request.data)
        srz_order = OrderSerializer(instance=self.order)
        now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
        if data.is_valid():
            try:
                coupon = Coupon.objects.get(code__exact=data.validated_data['code'],valid_from__lte=now,valid_to__gte=now,is_active=True)
            except Coupon.DoesNotExist:
                return Response({'error':'Coupon not found'},status=status.HTTP_404_NOT_FOUND)
            self.order.discount = coupon.discount
            self.order.save()
            return Response({'order':srz_order.data,'total_price':self.order.get_total_price()},status=status.HTTP_200_OK)


class ZarinPalPaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            description = serializer.validated_data['description']
            email = serializer.validated_data.get('email')
            mobile = serializer.validated_data.get('mobile')

            # Zarin Pal portal information
            merchant_id = settings.ZARINPAL_MERCHANT_ID
            url = "https://api.zarinpal.com/pg/v4/payment/request.json"

            # Make a payment request
            data = {
                "merchant_id": merchant_id,
                "amount": amount,
                "description": description,
                "email": email,
                "mobile": mobile,
                "callback_url": "http://your_callback_url",
            }

            response = requests.post(url, json=data)
            result = response.json()

            if result['data']['code'] == 100:
                # Successful application
                return Response({'payment_url': f"https://www.zarinpal.com/pg/StartPay/{result['data']['authority']}"},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': result['data']['message']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


