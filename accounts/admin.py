from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'password_info')

    def password_info(self, obj):
        return f"Salt: {obj.password.split('$')[2]}, Hash: {obj.password.split('$')[-1]}"
    password_info.short_description = 'Password Info'

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)