from django.urls import path

from . import views

app_name = 'rate'
urlpatterns = [
    path('', views.index, name='index'),
    path('review/', views.review, name='review'),
]
