from django.db import models
from django.shortcuts import reverse

#defining genres
recipe_choices= [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('dessert', 'Dessert'),
    ('appetizer', 'Appetizer'),
]

# Create your models here.
class Recipe(models.Model):
    name= models.CharField(max_length=120)
    description = models.TextField()
    cooking_time= models.FloatField(help_text= 'in minutes')
    ingredients= models.CharField(max_length=500, help_text='Ingredients must be separated by commas.')
    category= models.CharField(max_length=12, choices=recipe_choices, default='breakfast') 
    pic = models.ImageField(upload_to='customers', default='no_picture.jpg')
    
    # calculate difficulty of recipe using cooking time and number of ingredients
    def calculate_difficulty(self):
        ingredients = self.ingredients.split(', ')
        if self.cooking_time < 10 and len(ingredients) < 4:
            difficulty = 'Easy'
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = 'Hard'
        return difficulty
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
       return reverse ('recipes:detail', kwargs={'pk': self.pk})
