from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    DoctorModel,
    SpecialtyModel,
    DoctorNotesModel,
    BlogModel,
    CategoryModel,
    TagModel,
    CommentModel,
    BlogLikesModel,
)

class DoctorModel_Admin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_specialties']
    search_field = ['id']
    ordering = ['-user__id']

    def get_specialties(self, obj):
        return ', '.join([specialty.title for specialty in obj.specialties.all()])
    get_specialties.short_description = _('تخصص‌ها')
    

class SpecialtyModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']

class BlogModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'get_full_name', 'is_published', 'j_created']
    search_field = ['title', 'get_full_name', 'is_published']
    ordering = ['-id']

class CategoryModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']

class TagModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']

class DoctorNotesModel_Admin(admin.ModelAdmin):
    list_display = ['short_title', 'get_full_name']
    search_field = ['short_title', 'get_full_name']
    ordering = ['-id']

class CommentModel_Admin(admin.ModelAdmin):
    list_display = ['id', 'j_created']
    ordering = ['-id']

admin.site.register(DoctorModel, DoctorModel_Admin)
admin.site.register(SpecialtyModel, SpecialtyModel_Admin)
admin.site.register(DoctorNotesModel, DoctorNotesModel_Admin)
admin.site.register(BlogModel, BlogModel_Admin)
admin.site.register(CategoryModel, CategoryModel_Admin)
admin.site.register(TagModel, TagModel_Admin)
admin.site.register(CommentModel, CommentModel_Admin)
admin.site.register(BlogLikesModel)