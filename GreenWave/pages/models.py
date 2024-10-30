from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class user_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userprofile", null=True)
    image = models.ImageField(upload_to = 'profile_images/')
    school = models.CharField(max_length=200)
    year = models.IntegerField()
    major1 = models.CharField(max_length=200)
    major2 = models.CharField(max_length=200, blank = True, null = True)

class campaign(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    points = models.IntegerField()
    validation = models.CharField(max_length=200)
    description = models.TextField()

class service(models.Model):
    name = models.CharField(max_length = 20)
    image = models.ImageField(upload_to='service_images/')
    desc = models.CharField(max_length = 100)
    how_to_use = models.CharField(max_length = 100)
    why_to_use = models.CharField(max_length = 100)
    points_per_use = models.IntegerField()

    def __str__(self):
        return self.name
