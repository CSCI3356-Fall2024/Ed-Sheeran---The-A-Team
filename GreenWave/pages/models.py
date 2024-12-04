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
    points = models.IntegerField(default=0)

class Place(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class campaign(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    points = models.IntegerField()
    validation = models.CharField(max_length=200)
    description = models.TextField()
    places = models.ManyToManyField(Place)

    def __str__(self):
        return self.name

class service(models.Model):
    name = models.CharField(max_length = 20)
    id = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='service_images/')
    desc = models.CharField(max_length = 100)
    how_to_use = models.CharField(max_length = 100)
    why_to_use = models.CharField(max_length = 100)
    points_per_use = models.IntegerField()
    link = models.URLField(max_length = 200)

    def __str__(self):
        return self.name

class reward(models.Model): #these are the rewards users can get
    name = models.CharField(max_length = 25)
    #id = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='reward_images/')
    desc = models.CharField(max_length = 100)
    cost = models.IntegerField()
    places = models.ManyToManyField(Place)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class score(models.Model):
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.score}"

class transaction(models.Model): #think this works for transactions, trying to implement a model for transaction history
    user_profile = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name="trans")
    points = models.IntegerField()
    new_total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    place = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.points} points at {self.place} on {self.date} for {self.description}"

    class Meta:
        ordering = ['-date']
