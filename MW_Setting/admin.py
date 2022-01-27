from django.contrib import admin
from .models import BrandsModel, SettingModel, ContactUsModel, NewsEmailModel


class BrandsModel_Admin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ['-id']

class SettingModel_Admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']

class ContactUsModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'email']
    ordering = ['-id']

class NewsEmailModel_Admin(admin.ModelAdmin):
    list_display = ['email']
    ordering = ['-id']


admin.site.register(BrandsModel, BrandsModel_Admin)
admin.site.register(SettingModel, SettingModel_Admin)
admin.site.register(ContactUsModel, ContactUsModel_Admin)
admin.site.register(NewsEmailModel, NewsEmailModel_Admin)