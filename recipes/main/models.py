from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from main.slug import unique_slugify

from django.db import models

# Create your models here.

class Ingredients(models.Model):
    name = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Ingredients"
        
    def get_absolute_url(self):
        return reverse ('main.views.recipelist')
        
    
class Recipe(models.Model):
    name = models.CharField(max_length=300)
    ingredients = models.ManyToManyField("main.Ingredients")
    directions = models.TextField()
    slug = models.SlugField(unique=True)
    recipe_link = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='media')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse ('main.views.recipelist')
    
    def save(self, **kwargs):
        slug = '%s' % (self.name)
        unique_slugify(self, slug)
        super(Recipe, self).save()
