from django.contrib import admin
from . models import Category, Entry #, UserCategory
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind')

admin.site.register(Category, CategoryAdmin)

admin.site.register(Entry)

# obsolete
# admin.site.register(UserCategory)