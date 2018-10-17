from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import MincePie, Review
from .forms import MincePieForm, ReviewForm


def index(request):
    recent_mince_pie_list = MincePie.objects.order_by('-created_at')[:5]
    context = {
        'active_page' : 'index',
        'recent_mince_pie_list' : recent_mince_pie_list
    }
    return render(request, 'rate/index.html', context)

def overview(request):
    mince_pie_list = MincePie.objects.all()
    context = {
        'active_page' : 'overview',
        'mince_pie_list' : mince_pie_list
    }
    return render(request, 'rate/overview.html', context)

def submit_review(request, mince_pie_id):
    form = ReviewForm(request.POST)
    mince_pie_instance = get_object_or_404(MincePie, pk=mince_pie_id)

    if form.is_valid():
        pastry_rating = form.cleaned_data['pastry_rating']
        filling_rating = form.cleaned_data['filling_rating']
        appearance_rating = form.cleaned_data['appearance_rating']
        aroma_rating = form.cleaned_data['aroma_rating']
        value_for_money_rating = form.cleaned_data['value_for_money_rating']
        free_text_review = form.cleaned_data['free_text_review']
        review_instance = Review(mince_pie=mince_pie_instance,
                                 pastry_rating=pastry_rating,
                                 filling_rating=filling_rating,
                                 appearance_rating=appearance_rating,
                                 aroma_rating=aroma_rating,
                                 value_for_money_rating=value_for_money_rating,
                                 free_text_review=free_text_review,
                                 created_by=request.user)
        review_instance.save()
        return HttpResponseRedirect(reverse('detail', args=(mince_pie_instance.pk,)))
    
    return render(request, 'rate/detail.html', {'form' : form, 'mince_pie': mince_pie_instance})

def detail(request, mince_pie_id):
    form = ReviewForm()
    mince_pie = get_object_or_404(MincePie, pk=mince_pie_id)
    return render(request, 'rate/detail.html', {'form' : form, 'mince_pie': mince_pie})

def add_mince_pie(request):
    if request.method == 'POST':
        form = MincePieForm(request.POST)

        if form.is_valid():
            brand = form.cleaned_data['brand']
            name = form.cleaned_data['name']
            mince_pie_instance = MincePie(brand=brand, name=name, created_by=request.user)
            mince_pie_instance.save()
            return HttpResponseRedirect(reverse('detail', args=(mince_pie_instance.pk,)))
    else:
        form = MincePieForm()

    context = {
        'form' : form,
        'active_page' : 'add_mince_pie',
    }
    return render(request, 'rate/add_mince_pie.html', context)
