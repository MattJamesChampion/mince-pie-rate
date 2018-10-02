from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import MincePie


def index(request):
    mince_pie_list = MincePie.objects.all()
    context = {
        'mince_pie_list' : mince_pie_list
    }
    return render(request, 'rate/index.html', context)

def review(request):
    return render(request, 'rate/review.html')

def detail(request, mince_pie_id):
    mince_pie = get_object_or_404(MincePie, pk=mince_pie_id)
    return render(request, 'rate/detail.html', {'mince_pie': mince_pie})
