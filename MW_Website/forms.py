from django import forms
from django.db.models import fields
from .models import CommentModel

class CommentForm(forms.ModelForm):
    at_blog = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = CommentModel
        fields = ['message', 'at_blog']