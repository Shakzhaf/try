from django.db import models
 
# Create your models here.
 
 
class Article(models.Model):
    title = models.CharField(max_length=100)
    author =models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
 
 
    def __str__(self):
        return self.title

"""
from django.db import models

# Create your models here.

class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Article(models.Model):
    position = models.FotreignKey(Position, max_length=100)
    author =models.CharField(max_length=100, null='True',  blank='True')
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
 
    
"""