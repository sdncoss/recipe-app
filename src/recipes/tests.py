from django.test import TestCase
from .models import Recipe

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(
            name='Coffee',
            description='A warm beverage to enjoy in the morning',
            cooking_time=10,
            ingredients='Water, Coffee Grounds, Sugar, Cream'
        )
    
    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        
        field_label = recipe._meta.get_field('name').verbose_name
        
        self.assertEqual(field_label, 'name')
        
    def test_description(self):
        recipe = Recipe.objects.get(id=1)
        
        field_label = recipe._meta.get_field('description').verbose_name
        
        self.assertEqual(field_label, 'description')
        
    def test_cooking_time_is_integer(self):
        recipe = Recipe.objects.get(id=1)
        self.assertIsInstance(recipe.cooking_time, (int, float))
        
    def test_ingredients(self):
        recipe = Recipe.objects.get(id=1)
        
        field_label = recipe._meta.get_field('ingredients').verbose_name
        
        self.assertEqual(field_label, 'ingredients')
        
        
    def test_calculate_difficulty_hard(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.calculate_difficulty(), 'Hard')