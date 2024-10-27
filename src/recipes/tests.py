from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from .forms import RecipeSearchForm
from django.contrib.auth.models import User

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

    
class RecipeFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data_valid = {
            'name': 'Pasta',
            'ingredients': 'Tomato, Cheese',
            'max_cooking_time': 30,
            'difficulty': 'easy',  # Adjust according to your form definition
            'category': 'lunch',
        }

    def test_valid_form(self):
        form = RecipeSearchForm(data=self.form_data_valid)
        print(form.errors)  # Print the errors to the console
        self.assertTrue(form.is_valid())

class RecipeSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def test_search_view_authenticated(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search_results.html')

    def test_search_view_not_authenticated(self):
        self.client.logout()  # Ensure the user is logged out
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login