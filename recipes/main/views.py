from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from slugify import slugify

from .forms import RecipeForm, IngredientForm
from .models import Recipe, Ingredients

# Create your views here.

def recipe_list_API_view(request):
    recipes = Recipe.objects.all()
    output = serializers.serialize('json', recipes, fields=('name','ingredients','directions'))
    return HttpResponse(output, content_type='application/json')


def home(request):
    recipes = Recipe.objects.all()
    ingredients = 






def recipelist(request):
    recipes = Recipe.objects.all()

    context = {}

    for recipe in recipes:

        recipe.title = recipe.name

    context['recipe_list'] = recipes

    return render(request, 'recipelist.html', context)

# LISTVIEW WILL NOT WORK WITH "POST"  it will with GET but not POST
#class RecipeListView(ListView):
#    model = Recipe
#    template_name = "recipelist.html"
#    context_object_name = "recipe_list"
    
    
class RecipeDetailView(DetailView):
    model = Recipe
    slug_field = "slug"
    template_name = "ingredients.html"
    context_object_name = "recipe"


class RecipeCreateView(CreateView):
    form_class = RecipeForm
    template_name = "recipecreate.html"
    
    
class IngredientCreateView(CreateView):
    form_class = IngredientForm
    template_name = "ingredientcreate.html"