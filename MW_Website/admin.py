from django.contrib import admin
from django.contrib.admin.helpers import AdminField
from .models import (
    DoctorModel,
    SpecialtyModel,
    PatientModel,
    DoctorNotesModel,
    BlogModel,
    CategoryModel,
    TagModel,
    CommentModel,
    BlogLikesModel,
    CommentLikesModel,
)

class DoctorModel_Admin(admin.ModelAdmin):
    list_display = ['get_full_name', 'code']
    search_field = ['code']
    ordering = ['-user__id']

class SpecialtyModel_Admin(admin.ModelAdmin):
    list_display = ['title']
    search_field = ['title']
    ordering = ['-id']

class PatientModel_Admin(admin.ModelAdmin):
    list_display = ['get_full_name', 'code']
    search_field = ['code']
    ordering = ['-user__id']

class BlogModel_Admin(admin.ModelAdmin):
    list_display = ['title', 'get_full_name', 'is_published']
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
    list_display = ['__str__']
    ordering = ['-id']

admin.site.register(DoctorModel, DoctorModel_Admin)
admin.site.register(SpecialtyModel, SpecialtyModel_Admin)
admin.site.register(PatientModel, PatientModel_Admin)
admin.site.register(DoctorNotesModel, DoctorNotesModel_Admin)
admin.site.register(BlogModel, BlogModel_Admin)
admin.site.register(CategoryModel, CategoryModel_Admin)
admin.site.register(TagModel, TagModel_Admin)
admin.site.register(CommentModel, CommentModel_Admin)
admin.site.register(BlogLikesModel)
admin.site.register(CommentLikesModel)