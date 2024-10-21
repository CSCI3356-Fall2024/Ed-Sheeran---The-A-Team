from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class user_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userprofile", null=True)
    image = models.ImageField()
    school = models.CharField(max_length=200)
    year = models.IntegerField()
    major1 = models.CharField(max_length=200)
    major2 = models.CharField(max_length=200)