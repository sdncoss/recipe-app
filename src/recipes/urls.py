from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, RecipeListView, RecipeDetailView, SuccessView

app_name = 'recipes'

urlpatterns = [
   path('', home, name='home'),
   path('list/', RecipeListView.as_view(), name='list'),
   path('list/<int:pk>', RecipeDetailView.as_view(), name='detail'),
   path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
   path('logout/', LogoutView.as_view(next_page='recipes:success'), name='logout'),
   path('success/', SuccessView.as_view(), name='success'),
]