from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RecipeSearchForm, RecipeForm
import pandas as pd

# Create your views here.
@login_required
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/main.html', {'recipes': recipes})


class RecipeListView(LoginRequiredMixin, ListView):
   model = Recipe
   template_name = 'recipes/main.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
   model = Recipe
   template_name = 'recipes/detail.html'

class RecipeSearchView(LoginRequiredMixin, View):
    def get(self, request):
        form = RecipeSearchForm(request.GET or None)
        recipes = Recipe.objects.all()

        # Filter based on search criteria if the form is valid
        if form.is_valid():
            name = form.cleaned_data.get('name')
            ingredients = form.cleaned_data.get('ingredients')
            max_cooking_time = form.cleaned_data.get('max_cooking_time')
            category = form.cleaned_data.get('category')

            if name:
                recipes = recipes.filter(name__icontains=name)
            if ingredients:
                ingredient_list = ingredients.split(',')
                for ingredient in ingredient_list:
                    recipes = recipes.filter(ingredients__icontains=ingredient.strip())
            if max_cooking_time:
                recipes = recipes.filter(cooking_time__lte=max_cooking_time)
            if category:
                recipes = recipes.filter(category__icontains=category)

        # Convert the QuerySet to a DataFrame
        recipe_df = pd.DataFrame(list(recipes.values('id', 'name', 'cooking_time', 'category', 'description')))

        # Ensure the DataFrame has data before modifying
        if not recipe_df.empty:
            # Make recipe names clickable links to details page
            recipe_df['name'] = recipe_df.apply(
                lambda row: f'<a href="/list/{row["id"]}">{row["name"]}</a>', axis=1
            )

        recipe_table = recipe_df.to_html(classes="table table-striped", escape=False, index=False)

        return render(request, 'recipes/search_results.html', {'form': form, 'recipe_table': recipe_table})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes:list')  # Redirect to the recipe list after submission
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/add_recipe.html', {'form': form})