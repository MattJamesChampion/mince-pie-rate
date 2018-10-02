from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import MincePie, Review


def index(request):
    mince_pie_list = MincePie.objects.all()
    context = {
        'mince_pie_list' : mince_pie_list
    }
    return render(request, 'rate/index.html', context)

def review(request, mince_pie_id):
    mince_pie_instance = get_object_or_404(MincePie, pk=mince_pie_id)
    try:
        numeric_rating = int(request.POST['numeric_rating'])
        review_instance = Review(mince_pie=mince_pie_instance, rating=numeric_rating)
        review_instance.save()
    except Exception:
        error_message = 'Error - Could not create the review'
        return render(request, 'rate/detail.html', {'mince_pie' : mince_pie_instance, 'error_message' : error_message})
    else:
        return HttpResponseRedirect(reverse('rate:detail', args=(mince_pie_instance.pk,)))

def detail(request, mince_pie_id):
    mince_pie = get_object_or_404(MincePie, pk=mince_pie_id)
    return render(request, 'rate/detail.html', {'mince_pie': mince_pie})
