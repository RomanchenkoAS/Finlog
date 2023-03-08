from django.db import models
from django.contrib.auth.models import AbstractUser
from log.models import Category

# Custom user model containing a list of categories and according methods
class User(AbstractUser):
    
    def generate_categories(self):
        # Add all the default categories to the user
        list = Category.objects.all()
        
        for item in list:
            UserCategory.objects.add()

    def get_user_categories(self):
        return UserCategory.objects.filter(user=self)

    def add_user_category(self, name):
        user_category = UserCategory.objects.create(name=name, user=self)
        return user_category

    def remove_user_category(self, user_category):
        user_category.delete()
    
class UserCategory(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default='#d3d3d3')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
