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
        '''If the DB requires deleting of all categories, calling this will generate them'''
        list = [
            ('Housing',         '#ffbe0b'),
            ('Transportation',  '#fb5607'),
            ('Food',            '#2a9d8f'),
            ('Entertainment',   '#ff006e'),
            ('Health',          '#8338ec'),
            ('Savings',         '#3a86ff'),
        ]
                
        for item in list:
            x, y = item
            a = Category.objects.create(name=x, color=y)
            a.save()
            