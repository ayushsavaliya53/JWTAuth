from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    OTPSerializer
)
from .models import (
    OTPModel
)
from rest_framework import generics
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view
from JWTAUth.settings import EMAIL_HOST_USER, SECRET_KEY as secret_key
import jwt
from jwt import ExpiredSignatureError
from django.core.mail import send_mail
import random
from datetime import datetime, timedelta

def get_token(is_new, username, email, password):
    user = None
    if is_new:
        user = User.objects.create(username = username, email = email)
        user.set_password(password)
        user.save()
    else:
        user = authenticate(username = username, email = email, password = password)

    if user:
        token = AccessToken.for_user(user)
        return Response({'token': str(token)})
            
    else:
        return Response({"message": "Invalid credentials"})


@api_view(['POST', 'GET'])
def UserView(req):
    if req.method == 'GET':
        try:
            token = req.headers.get('Authorization')
            if token.startswith("Bearer "):
                token = token.split("Bearer ")[1]
            elif not token:
                return Response({'message' : 'no token fetched'})
            else:
                return Response({'message' : 'invalid token'})
            
            decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])

            user_id = decoded_payload.get('user_id', 'unknown')
            user = User.objects.get(id = user_id)

            return Response({"message": f"Hello {user}, You are logged in!"})

        except ExpiredSignatureError:
            return Response({"error": "Token has expired"})
        except Exception as e:
            return Response({"message": f"{e}"})

    return Response({'message': "UserView"})

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    def post(self, req):
        email = req.data.get('email')
        username = req.data.get('username')
        password = req.data.get('password')
        email_exists = User.objects.filter(email = email).exists()
        user_exists = User.objects.filter(username = username).exists()
        if email_exists:
            return Response({'message' : "Email Already Used"})
        elif user_exists:
            return Response({{'message' : "User Already Exists"}})
        else:
            otp = str(random.randint(100000, 999999))
            subject = 'OTP for verification'
            message = f'Your OTP is {otp}'
            from_email = EMAIL_HOST_USER
            to_email = email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)
            expiry_time = datetime.now() + timedelta(minutes=5)
            otprow = OTPModel.objects.create(username = username, email = email, password = password, otp = otp, expirytime = expiry_time)
            otprow.save()
            return redirect('otp-view', user=username)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, req):
        username = req.data.get('username')
        email = req.data.get('email')
        password = req.data.get('password')
        return get_token(0, username, email, password)

class OTPView(generics.GenericAPIView):
    serializer_class = OTPSerializer
    def post(self, request, *args, **kwargs):
        username = kwargs['user']

        user = OTPModel.objects.filter(username = username).last()
        if user:
            expiry = user.expirytime
            otp = user.otp
            email = user.email
            password = user.password
        else:
            return Response({'message' : "Invalid Access"})


        if not otp or not expiry:
            return Response({'message': 'Session expired or invalid'})
        

        if datetime.now(expiry.tzinfo) > expiry:
            return Response({'message' : 'OTP has expired'})
        
        else:
            if otp == request.data.get('otp'):
                return get_token(1,username, email, password)
            else:
                return Response({'message' : 'Invalid OTP'})