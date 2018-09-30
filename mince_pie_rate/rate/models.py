from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class MincePie(models.Model):
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{0} - {1}".format(self.brand, self.name)

class Review(models.Model):
    mince_pie = models.ForeignKey(MincePie, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return "{0}: {1}".format(str(self.mince_pie), self.rating)
