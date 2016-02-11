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
    ingredients = Ingredients.objects.all()
    
    context = {}
        
    context['recipe_list'] = recipes
    
    context['ingredient_list'] = ingredients
    
    return render(request, 'home.html', context)


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
    

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['title', 'body',])
        
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

    return render_to_response('search/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))