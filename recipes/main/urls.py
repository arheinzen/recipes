from django.conf.urls import include, url
from django.conf import settings
from django.views.generic import TemplateView

from .views import RecipeDetailView, RecipeCreateView, IngredientCreateView


urlpatterns = [
    
    url(r'^recipe_list_API/$', 'main.views.recipe_list_API_view'),
    url(r'^recipelist/$', 'main.views.recipelist'),
    url(r'^recipelist/(?P<slug>.+)/$', RecipeDetailView.as_view()),
    url(r'^recipecreate/$', RecipeCreateView.as_view()),
    url(r'^recipesuccess/$', TemplateView.as_view(template_name="recipe_success.html")),
    url(r'^home/$', TemplateView.as_view(template_name="home.html")),
    url(r'^ingredientcreate/$', IngredientCreateView.as_view()),
    
]