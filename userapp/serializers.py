from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(required = True)
    email = serializers.EmailField()
    password = serializers.CharField(required = True, write_only = True)


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required = True, write_only = True)