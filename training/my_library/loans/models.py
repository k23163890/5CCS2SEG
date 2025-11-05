from django.db import models

# Create your models here.

class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()

    

    
