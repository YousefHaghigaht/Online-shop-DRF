from rest_framework import serializers
from .models import User


def clean_email(value):
    """
    Email field validator
    """
    if 'admin' in value:
        raise serializers.ValidationError('The email entered should not be admin')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializing user fields :
    phone number , email , full name , password , confirm password
    """
    confirm_password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['phone_number','email','full_name','password','confirm_password']
        extra_kwargs = {
            'password':{'write_only':True},
            'email':{'validators':(clean_email,)},
        }

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)

    def validate_phone_number(self,value):
        if len(value) != 11:
            raise serializers.ValidationError('The phone number must have 11 length')
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords dont match')
        return data

class VerifyCodeRegister(serializers.Serializer):
    code = serializers.IntegerField()

