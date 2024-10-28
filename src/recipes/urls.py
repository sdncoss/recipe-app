from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, RecipeListView, RecipeDetailView, RecipeSearchView, add_recipe

app_name = 'recipes'

urlpatterns = [
   path('', home, name='home'),
   path('list/', RecipeListView.as_view(), name='list'),
   path('list/<int:pk>', RecipeDetailView.as_view(), name='detail'),
   path('search/', RecipeSearchView.as_view(), name='search'),
   path('add/', add_recipe, name='add'),
   path('login/', LoginView.as_view(template_name='auth/login.html', redirect_authenticated_user=True), name='login'),
   path('logout/', LogoutView.as_view(template_name='recipes/success.html'), name='logout'),
]