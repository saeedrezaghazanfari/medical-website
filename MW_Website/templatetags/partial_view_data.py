from django import template
from MW_Website.models import BlogModel, DoctorNotesModel, DoctorModel, CategoryModel
from MW_Setting.models import BrandsModel


register = template.Library()

@register.simple_tag
def doctor_notes():
    notes = DoctorNotesModel.objects.all()[:6]
    if notes:
        return notes
    return None

@register.simple_tag
def doctor_cards():
    cards = DoctorModel.objects.all()[:3]
    if cards:
        return cards
    return None

@register.simple_tag
def brands_footer():
    logos = BrandsModel.objects.all()[:20]
    if logos:
        return logos
    return None

@register.simple_tag
def last_categories():
    categories = CategoryModel.objects.all()
    if categories:
        return categories
    return None

@register.simple_tag
def last_posts():
    blogs = BlogModel.objects.filter(is_published=True).all()[:4]
    if blogs:
        return blogs
    return None