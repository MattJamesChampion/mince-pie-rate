from django.http import HttpResponse
from django.shortcuts import render

from .models import MincePie


def index(request):
    mince_pie_list = MincePie.objects.all()
    context = {
        'mince_pie_list' : mince_pie_list
    }
    return render(request, 'rate/index.html', context)

def review(request):
    return render(request, 'rate/review.html')
