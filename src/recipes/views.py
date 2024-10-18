from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_home.html', {'recipes': recipes})

class RecipeListView(ListView):
   model = Recipe
   template_name = 'recipes/main.html'

class RecipeDetailView(DetailView):
   model = Recipe
   template_name = 'recipes/detail.html'