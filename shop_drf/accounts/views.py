from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import status
from .models import OtpCode,User
import random
from datetime import datetime,timedelta
import pytz


class UserRegisterView(APIView):
    """
    Save  phone number , email , full name , password , confirm password fields
    in the session and send SMS to the phone number

    and

    Create a code in the OtpCode model
    fields :  phone number , code , created
    """
    def post(self,request):
        srz_data = serializers.UserRegisterSerializer(data=request.POST)
        if srz_data.is_valid():
            sv = srz_data.validated_data
            request.session['user_registration_info'] = {
                'phone_number':sv['phone_number'],
                'email':sv['email'],
                'full_name':sv['full_name'],
                'password':sv['password']
            }
            random_code = random.randint(1000,9999)
            OtpCode.objects.create(phone_number=sv['phone_number'],code=random_code)
            return Response(data={'message':'We send a code to your phone number','session':srz_data.data},status=status.HTTP_200_OK)
        return Response(data={'user':srz_data.errors},status=status.HTTP_400_BAD_REQUEST)


class VerifyRegisterView(APIView):
    """
    Checking the equality and expiration of the entered code with the code stored in the OtpCode model
    field:
    Code
    """

    def post(self,request):
        user_session = request.session['user_registration_info']
        srz_data = serializers.VerifyCodeRegister(data=request.POST)
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        if srz_data.is_valid():
            if srz_data.validated_data['code'] == code_instance.code:
                User.objects.create_user(phone_number=user_session['phone_number'],email=user_session['email'],
                                         full_name=user_session['full_name'],password=user_session['password'])
                code_instance.delete()
                return Response(data={'message':'User registered'},status=status.HTTP_200_OK)
            else:
                return Response(data={'message':'The entered code is not correct'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response(data=srz_data.errors,status=status.HTTP_400_BAD_REQUEST)






