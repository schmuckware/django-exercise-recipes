from django.db import models

# Create your models here.

MEAL_TYPES = [
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Other', 'Other'),
]


class Recipe(models.Model):
    image = models.ImageField(upload_to='static/images', blank=True, default='static/images/pineapple_rubix.png')
    name = models.CharField(max_length=45)
    mealType = models.CharField(choices=MEAL_TYPES, default='Other', max_length=10)
    description = models.TextField(blank=True, max_length=200)
    directions = models.TextField(blank=True)
    prepTime = models.IntegerField(blank=True, default=0)
    cookTime = models.IntegerField(blank=True, default=0)
    standTime = models.IntegerField(blank=True, default=0)
    # More emphasis -> recipe appears more often in plan
    emphasis = models.FloatField(blank=True, default=1.0)
