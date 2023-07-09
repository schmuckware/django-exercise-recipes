"""
URL configuration for recipesV2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from recipe.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main dashboard
    path('dashboard', get_recipe_list, name='recipe_list'),
    path('index', get_recipe_list, name='recipe_list'),
    path('recipe', get_recipe_list, name='recipe_list'),
    path('', get_recipe_list, name='recipe_list'),

    # Recipe information and operations
    path('recipe/<int:pk>/', get_recipe_detail, name='recipe_detail'),
    path('recipe/add', maintain_recipe, name='add_recipe'),
    path('recipe/edit/<int:pk>', maintain_recipe, name='edit_recipe'),
    path('recipe/delete/<int:pk>', delete_recipe, name='delete recipe'),

    # Additional functionality
    path('search/', search_recipes, name='search_recipes'),
    path('discover/', discover_recipe, name='discover_recipe'),
    path('generate-meal-plan', meal_plan, name='meal_plan'),
]
