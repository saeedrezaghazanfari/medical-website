from django import template
from MW_Website.models import DoctorNotesModel, DoctorModel


register = template.Library()

@register.simple_tag
def doctor_notes():
    notes = DoctorNotesModel.objects.all()[:6]
    if notes:
        return notes
    return False

@register.simple_tag
def doctor_cards():
    notes = DoctorModel.objects.all()[:3]
    if notes:
        return notes
    return False