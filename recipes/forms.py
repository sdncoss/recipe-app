from django import forms
from .models import Recipe

class RecipeSearchForm(forms.Form):
    name = forms.CharField(max_length=120, required=False, label="Recipe Name")
    ingredients = forms.CharField(max_length=500, required=False, label="Ingredients (comma-separated)")
    max_cooking_time = forms.IntegerField(required=False, label="Max Cooking Time (minutes)")
    category= forms.ChoiceField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('dessert', 'Dessert'), ('appetizer', 'Appetizer')], required=False)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cooking_time', 'ingredients', 'category', 'pic']