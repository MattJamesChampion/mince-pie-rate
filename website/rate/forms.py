from django import forms
from . import models

class MincePieForm(forms.ModelForm):
    class Meta:
        model = models.MincePie
        fields = ['brand', 'name', 'box_image','box_back_image', 'mince_pie_image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['pastry_rating', 'filling_rating', 'appearance_rating', 'aroma_rating', 'value_for_money_rating', 'free_text_review']
