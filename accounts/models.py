from django.db import models
from django.contrib.auth.models import AbstractUser
from log.models import Category

class

# Custom user model containing a list of categories and according methods
class User(AbstractUser):
    categories = models.ManyToManyField('Category', blank=True)
    
    def generate_categories(self):
        # Add all the default categories to the user
        list = Category.objects.all()
        self.categories.add(list)

    def get_categories(self):
        return self.categories.all()