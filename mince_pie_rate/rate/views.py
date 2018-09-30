from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Welcome to Mince Pie-Rate. Yarr!")
