from django.urls import path

from . import views

app_name = 'rate'
urlpatterns = [
    path('', views.index, name='index'),
    path('mince-pies/', views.overview, name='overview'),
    path('mince-pies/<int:mince_pie_id>', views.detail, name='detail'),
    path('mince-pies/<int:mince_pie_id>/review/', views.review, name='review'),
    path('mince-pies/add/', views.add, name='add'),
    path('mince-pies/add/submit/', views.submit_add, name='submit_add'),
]
