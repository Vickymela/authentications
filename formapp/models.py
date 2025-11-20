from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.

class Otp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.IntegerField()
    status= models.BooleanField(default=False)

    created_when = models.DateTimeField(auto_now_add=True)

    def  __str__(self):
        return f"password reset for {self.user.username} at {self.created_when}"




