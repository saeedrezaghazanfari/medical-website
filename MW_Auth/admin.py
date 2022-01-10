from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class AdminUser(UserAdmin):
    UserAdmin.fieldsets[2][1]['fields'] = (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
        'user_permissions',
        'phone',
        'ip',
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'ip', 'phone')

admin.site.register(User, AdminUser)