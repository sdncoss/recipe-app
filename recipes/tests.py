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

class AddRecipeViewTest(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
    

    def test_add_recipe_page_renders_for_logged_in_user(self):
        # Logged-in user should see the add recipe page
        response = self.client.get(reverse('recipes:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')
        self.assertContains(response, 'Add Recipe')  # Verifying if page title or heading is present

    def test_add_recipe_successful_submission(self):
        # Data for creating a new recipe
        recipe_data = {
            'name': 'Chocolate Cake',
            'description': 'A delicious chocolate cake',
            'cooking_time': 45,
            'ingredients': 'Flour, Sugar, Cocoa, Baking Powder, Milk, Eggs',
            'category': 'dessert',
        }
        
        response = self.client.post(reverse('recipes:add'), data=recipe_data)
        
        # Verify that the form redirects to the recipe list page
        self.assertRedirects(response, reverse('recipes:list'))
        
        # Check that the recipe was actually created in the database
        self.assertEqual(Recipe.objects.count(), 1)
        new_recipe = Recipe.objects.first()
        self.assertEqual(new_recipe.name, 'Chocolate Cake')

    def test_add_recipe_invalid_submission(self):
        # Submit incomplete form data (missing required fields)
        incomplete_data = {
            'name': '',  # Name is required, so this will cause form validation to fail
            'description': 'Incomplete recipe',
            'cooking_time': 30,
        }
        
        response = self.client.post(reverse('recipes:add'), data=incomplete_data)
        
        # Ensure that the form returns to the add recipe page without redirect
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')
        
        # Check that no new recipes were added to the database
        self.assertEqual(Recipe.objects.count(), 0)
        self.assertContains(response, 'This field is required')  # Checks error message on form