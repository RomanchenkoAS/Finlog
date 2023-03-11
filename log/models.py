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
            ('Housing', '#add8e6'),
            ('Transportation', '#ff8080'),
            ('Food', '#90ee90'),
            ('Entertainment', '#ce7bce'),
            ('Self-care', '#add8e6'),
            ('Utilities', '#ffff00'),
            ('Clothing', '#ffa500'),
            ('Education', '#ffc0cb'),
            ('Medical', '#20b2aa'),
            ('Savings', '#808080'),
        ]
        
        for item in list:
            x, y = item
            a = Category.objects.create(name=x, color=y)
            a.save()
            print(f'Created {x}:{y}')
            