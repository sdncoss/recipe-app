from django.test import TestCase
from django.urls import reverse
from .models import Recipe

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(
            name='Coffee',
            description='A warm beverage to enjoy in the morning',
            cooking_time=5,
            ingredients='Water, Coffee Grounds, Cream',
            category='breakfast'
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
        self.assertEqual(recipe.calculate_difficulty(), 'Easy')

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        # The get_absolute_url() should return the correct URL for the recipe detail page
        self.assertEqual(recipe.get_absolute_url(), '/list/1')

    def test_home_page_contains_recipe_name(self):
        """Test that the home page contains the recipe name."""
        response = self.client.get(reverse('recipes:home'))
        self.assertContains(response, self.recipe.name)

    def test_links_on_home_page(self):
        """Test that links on the home page are present."""
        response = self.client.get(reverse('recipes:home'))
        self.assertContains(response, reverse('recipes:list'))
