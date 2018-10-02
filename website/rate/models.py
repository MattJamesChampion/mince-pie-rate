from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class MincePie(models.Model):
    created_by = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, related_name='mince_pie_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, related_name='mince_pie_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{0} - {1}".format(self.brand, self.name)

class Review(models.Model):
    created_by = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, related_name='review_created_by')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL, related_name='review_updated_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    mince_pie = models.ForeignKey(MincePie, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return "{0}: {1}".format(str(self.mince_pie), self.rating)
