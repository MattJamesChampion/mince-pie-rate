from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'rate/index.html')

def review(request):
    return render(request, 'rate/review.html')
