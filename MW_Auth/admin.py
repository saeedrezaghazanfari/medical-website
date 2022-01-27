from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User


class AdminUser(UserAdmin):
    UserAdmin.fieldsets[2][1]['fields'] = (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
        'user_permissions',
        'ip',
        'phone',
        'profile',
        'national_code'
    )
    list_display = ('username', 'email', 'get_full_name', 'phone', 'get_profile')

admin.site.register(User, AdminUser)
admin.site.unregister(Group)          # hide groups