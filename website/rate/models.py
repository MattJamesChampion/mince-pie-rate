from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from os.path import join, splitext
from urllib.parse import quote_plus

def box_image_path(instance, filename):
    base_file_name, file_extension = splitext(filename)
    return join(quote_plus(instance.brand), quote_plus(instance.name), "box_image" + file_extension.lower())

def mince_pie_image_path(instance, filename):
    base_file_name, file_extension = splitext(filename)
    return join(quote_plus(instance.brand), quote_plus(instance.name), "mince_pie_image" + file_extension.lower())

class MincePie(models.Model):
    created_by = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, related_name='mince_pie_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    box_image = models.FileField(upload_to=box_image_path, blank=True)
    mince_pie_image = models.FileField(upload_to=mince_pie_image_path, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.brand, self.name)

class Review(models.Model):
    created_by = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, related_name='review_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    mince_pie = models.ForeignKey(MincePie, on_delete=models.CASCADE)

    pastry_rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(10)])
    filling_rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(10)])
    appearance_rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(10)])
    aroma_rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(10)])
    value_for_money_rating = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(10)])

    free_text_review = models.TextField(max_length=1000, blank=True)

    @property
    def rating_total(self):
        return self.pastry_rating + self.filling_rating + self.appearance_rating + self.aroma_rating + self.value_for_money_rating

    @property
    def rating_mean(self):
        number_of_rating_fields = 5
        return self.rating_total / number_of_rating_fields

    def __str__(self):
        return "{0} : {1} : {2}".format(self.created_by, str(self.mince_pie), self.rating_total)
