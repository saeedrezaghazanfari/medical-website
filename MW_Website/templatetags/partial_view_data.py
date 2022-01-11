from django import template
from MW_Website.models import DoctorNotesModel, DoctorModel
from MW_Setting.models import BrandsModel


register = template.Library()

@register.simple_tag
def doctor_notes():
    notes = DoctorNotesModel.objects.all()[:6]
    if notes:
        return notes
    return False

@register.simple_tag
def doctor_cards():
    cards = DoctorModel.objects.all()[:3]
    if cards:
        return cards
    return False

@register.simple_tag
def brands_footer():
    logos = BrandsModel.objects.all()[:20]
    if logos:
        return logos
    return False