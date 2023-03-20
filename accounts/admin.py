from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserCategory, Entry


class UserAdmin(UserAdmin):
    '''To monitor user's password info (developement purposes)'''
    list_display = ('username', 'email', 'currency', 'budget', 'password_info')

    def password_info(self, obj):
        return f"Salt: {obj.password.split('$')[2]}, Hash: {obj.password.split('$')[-1]}"
    password_info.short_description = 'Password Info'

admin.site.register(User, UserAdmin)

class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'color', 'user')
    
admin.site.register(UserCategory, UserCategoryAdmin)

admin.site.register(Entry)
