from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_home.html', {'recipes': recipes})


class RecipeListView(LoginRequiredMixin, ListView):
   model = Recipe
   template_name = 'recipes/main.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
   model = Recipe
   template_name = 'recipes/detail.html'

class SuccessView(TemplateView):
    template_name = 'recipes/success.html'