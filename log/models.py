from django.db import models  # For basic models management


# Default categories
class Category(models.Model):
    '''Describes kinds of spending/income'''

    # Description of the spending/income type
    name = models.CharField(max_length=200)

    color = models.CharField(max_length=7, default='#d3d3d3')

    # Name
    def __str__(self):
        return self.name

    # For proper representation on admin page
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def generate_default(self):
        list = [
            ('Housing', '#ffbe0b'),
            ('Transportation', '#fb5607'),
            ('Food', '#2a9d8f'),
            ('Entertainment', '#ff006e'),
            ('Health', '#8338ec'),
            ('Savings', '#3a86ff'),
        ]
        
        # Updated default categories

# Housing: Includes rent/mortgage payments, property taxes, home insurance, and utilities.
# Transportation: Includes car payments, gas, insurance, and maintenance costs.
# Food and groceries: Includes all expenses related to food and groceries, including dining out, snacks, and beverages.
# Entertainment and leisure: Includes expenses for movies, hobbies, vacations, and other leisure activities.
# Health and wellness: Includes expenses for gym memberships, health and wellness products, and personal care services.
# Savings and investments: Includes contributions to emergency funds, retirement savings, and investment accounts.
        
        for item in list:
            x, y = item
            a = Category.objects.create(name=x, color=y)
            a.save()
            print(f'Created {x}:{y}')
            