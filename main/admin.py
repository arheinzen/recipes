from django.contrib import admin
from main.models import Ingredients, Recipe

# Register your models here.

#class IngredientsAdmin(admin.ModelAdmin):
#    list_display = ("name",)
#    search_fields = ["name"]
#    
#class RecipeAdmin(admin.ModelAdmin):
#    list_display = ("name",)
#    search_fields = ["name"]
    
    
admin.site.register(Ingredients)
admin.site.register(Recipe)
    
