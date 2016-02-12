import csv
import os
import sys
import requests
from PIL import Image
import urllib
import urllib2
from slugify import slugify
from django.core.files import File
sys.path.append("..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipes.settings")

import django
django.setup()

from main.models import Recipe, Ingredients

Recipe.objects.all().delete()
Ingredients.objects.all().delete()

api_key = "f226968bd5f4291fea9ea9e0caad65b8"

for x in range(1,10):
    
    param_dict = {'key': api_key, 'sort': 'r', 'page': x}
    response = requests.get('http://food2fork.com/api/search/recipes.json', params=param_dict)

    print response
    response = response.json()
    recipes = response['recipes']

for recipe in recipes:
    print recipe['title']
    recipe_id = recipe['recipe_id']
    param_dict = {'key': api_key, 'rId':recipe_id}
    response = requests.get('http://food2fork.com/api/get', params=param_dict)
    
    response = response.json()
    print response['recipe']['ingredients']
    ingredients = response['recipe']['ingredients']

    new_recipe, created = Recipe.objects.get_or_create(name=recipe['title'])
    print recipe
    print created
    print '******'
    print Ingredients
    new_recipe.name = recipe['title']
    new_recipe.slug = slugify(recipe['title'])
    new_recipe.recipe_link = recipe['source_url']
    print new_recipe.name
    

    image = urllib.urlretrieve(recipe['image_url'])
    new_recipe.image.save(os.path.basename(recipe['image_url']), File(open(image[0])))
    
    
    
    
    for ingredient in ingredients:
        print "*****"
        print ingredient
        new_ingredient, created = Ingredients.objects.get_or_create(name=ingredient)
        print "NEW INGREDIENT"
        print new_ingredient.name
        
        new_recipe.ingredients.add(new_ingredient)
        
        new_ingredient.save()
    
    
    new_recipe.save()   
    
    # new_ingredient, created = Ingredient.objects.get_or_create(name=ingredients['ingredients'])
    # new_ingredient.save()
    # new_image = urllib.urlretrieve(recipe['image_url'])
    # new_recipe.image.save(os.path.basename(recipe['image_url']), File(open(new_image[0])))