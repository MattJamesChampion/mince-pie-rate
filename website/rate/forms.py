from django import forms
from . import models

class MincePieForm(forms.ModelForm):
    class Meta:
        model = models.MincePie
        fields = ['brand', 'name']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'free_text_review']
