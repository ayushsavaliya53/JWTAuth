from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class image(models.Model):
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return f"Image {self.id}"
    

class OTPModel(models.Model):
    username = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    otp = models.TextField()
    expirytime = models.DateTimeField()
