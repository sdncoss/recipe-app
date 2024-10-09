from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    #define Users username
    username= models.CharField(max_length=120)
    #define Users name
    name= models.CharField(max_length=120)
    
    def __str__(self):
        return f"Profile of {self.user.username}" 