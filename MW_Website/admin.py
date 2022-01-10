from django.contrib import admin
from .models import DoctorModel


class DoctorModel_Admin(admin.ModelAdmin):
    # list_display = ['user__first_name', 'user__last_name', 'user__phone']
    search_field = ['code']
    ordering = ['-user__id']


admin.site.register(DoctorModel, DoctorModel_Admin)
