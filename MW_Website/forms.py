from django import forms
from django.db import models
from django.db.models import fields
from .models import CommentModel


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['message']
