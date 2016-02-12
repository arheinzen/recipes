from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from slugify import slugify

import re
from django.db.models import Q

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




def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query    
    

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        ingredients = get_query(query_string, ['title', 'body',])
        
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

    return render_to_response('search/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))