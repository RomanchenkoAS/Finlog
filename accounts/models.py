from django.db import models
from django.contrib.auth.models import AbstractUser
from log.models import Category, CURRENCY_CHOICES

# Custom user model containing a list of categories and according methods
class User(AbstractUser):
    
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, default='KZT')
    
    def generate_categories(self):
        # Add all the default categories to the user
        list = Category.objects.all()
        
        for item in list:
            UserCategory.objects.create(name=item.name, color=item.color, user=self)

    def get_user_categories(self):
        return UserCategory.objects.filter(user=self)

    def add_user_category(self, name, color):
        user_category = UserCategory.objects.create(name=name, color=color, user=self)
        return user_category

    def remove_user_category(self, user_category):
        user_category.delete()
        
    def save(self, *args, **kwargs):
        # Check if this is a new user - he has no primary key
        is_new = not self.pk  
        super().save(*args, **kwargs)
        if is_new:
            # Actually generate default categories list
            self.generate_categories()
    
class UserCategory(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default='#d3d3d3')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # For proper representation on admin page
    class Meta:
        verbose_name = "User category"
        verbose_name_plural = "User categories"
        
    # Name of the entry
    def __str__(self):
        title = f'{self.name} edited'
        return title
