from collections import defaultdict
from random import choices, randint

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from recipe.forms import *


# Create your views here.
def get_recipe_list(request):
    recipes_by_type = defaultdict(list)
    meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Other']

    # Sort by meal types, so we get different categories for the carousels
    for meal_type in meal_types:
        recipes = Recipe.objects.filter(mealType=meal_type).order_by('name')
        recipes_by_type[meal_type] = recipes

    return render(request, 'recipe/recipe_list.html', {
        'page_title': 'Dashboard',
        'recipes_by_type': recipes_by_type,
        'meal_types': meal_types
    })


def get_recipe_detail(request, pk):
    recipe = Recipe.objects.get(id=pk)
    # Grab all paragraphs from the directions column and remove empty strings
    directions_lines = [line for line in recipe.directions.splitlines() if line]
    return render(request, 'recipe/recipe_detail.html', {'page_title': 'Details',
                                                         'recipe': recipe, 'directions_lines': directions_lines})


def maintain_recipe(request, pk=None):
    # Switches between editing and adding
    if pk:
        recipe = Recipe.objects.get(pk=pk)
    else:
        recipe = Recipe()

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe saved.')
            return HttpResponseRedirect(reverse_lazy('recipe_list'))
        else:
            messages.error(request, 'Wrong data input')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipe/maintain_recipe.html', {'page_title': 'Editor',
                                                           'form': form, 'recipe': recipe})


def delete_recipe(request, pk):
    # Delete recipe through the primary key
    Recipe.objects.get(pk=pk).delete()
    messages.success(request, 'Recipe deleted.')
    # Redirect back to recipe dashboard
    return HttpResponseRedirect(reverse_lazy('recipe_list'))


def meal_plan(request):
    try:
        recipes = Recipe.objects.all()
        # Assign all recipes to meal type variables
        breakfast_recipes = recipes.filter(mealType='Breakfast')
        lunch_recipes = recipes.filter(mealType='Lunch')
        dinner_recipes = recipes.filter(mealType='Dinner')

        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        meal_plan_storage = []

        for day in days_of_week:
            # Randomly select recipes based on emphasis
            breakfast = choices(breakfast_recipes, k=1, weights=[recipe.emphasis for recipe in breakfast_recipes])[0]
            lunch = choices(lunch_recipes, k=1, weights=[recipe.emphasis for recipe in lunch_recipes])[0]
            dinner = choices(dinner_recipes, k=1, weights=[recipe.emphasis for recipe in dinner_recipes])[0]

            # Add the meal plan for the day
            meal_plan_storage.append({'day': day, 'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner})

        return render(request, 'recipe/meal_plan.html', {'page_title': 'Meal Plan', 'meal_plan': meal_plan_storage})
    except IndexError:
        messages.error(request, 'Not enough recipes in each category to generate a meal plan.')
        return HttpResponseRedirect(reverse_lazy('recipe_list'))


def search_recipes(request):
    q = request.GET.get('q')

    if not q:
        messages.error(request, 'Search query is empty')
        return HttpResponseRedirect(reverse_lazy('recipe_list'))

    # Match with recipe names
    recipes = Recipe.objects.filter(name__icontains=q)

    # Check if any recipe matches came back
    if recipes.exists():
        return render(request, 'recipe/search_recipes.html', {
            'page_title': 'Search',
            'recipes': recipes,
        })
    else:
        messages.error(request, 'No hits')
        # Redirect to a default page if no matching recipe is found or no search query is present
        return HttpResponseRedirect(reverse_lazy('recipe_list'))


def discover_recipe(request):
    recipe_count = Recipe.objects.count()
    index = randint(0, recipe_count - 1)
    recipe = Recipe.objects.all()[index]
    # List details of a random recipe
    return redirect('recipe_detail', pk=recipe.id)
