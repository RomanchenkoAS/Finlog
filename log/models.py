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

    
    # Obsolete remove TODO
    # Custom categories
# class UserCategory(models.Model):
#     # Who customized this category
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)

#     # Parent category (optional)
#     category = models.ForeignKey(
#         Category, on_delete=models.CASCADE, null=True, blank=True)

#     # Description of the spending/income type
#     name = models.CharField(max_length=200, null=True, blank=True)

#     # New color
#     color = models.CharField(max_length=7, default='#d3d3d3')

#     # Generate a title
#     def title(self):
#         return self.name.lower().replace(' ', '_').replace('-','_')

#     # Name
#     def __str__(self):
#         if self.category:
#             return f'{self.category} updated'
#         elif isinstance(self.name, str):
#             return self.name
#         else:
#             return '-'

#     # For proper representation on admin page
#     class Meta:
#         verbose_name = "User category"
#         verbose_name_plural = "User categories"