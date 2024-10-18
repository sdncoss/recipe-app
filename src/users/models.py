from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
	name= models.CharField(max_length=120)
	username= models.CharField(max_length=120)
	pic = models.ImageField(upload_to='users', default='no_picture.jpg')

	def __str__(self):
		return "Profile of " + str(self.username)