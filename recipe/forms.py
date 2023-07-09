from django.forms import *

from recipe.models import *


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ()
        labels = {'mealType': 'Meal type', 'prepTime': 'Preparation time', 'cookTime': 'Cooking time',
                  'standTime': 'Standing time'}
