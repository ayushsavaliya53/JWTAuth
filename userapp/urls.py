from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    UserView,
    OTPView,
)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('UserView/', UserView, name='user'),
    path('OTPView/<str:user>', OTPView.as_view(), name='otp-view')
]