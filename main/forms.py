from django import forms

from .models import Recipe, Ingredients


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'directions', 'image', 'recipe_link']
        
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['name']