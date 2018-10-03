from django.urls import path

from . import views

app_name = 'rate'
urlpatterns = [
    path('', views.index, name='index'),
    path('mince-pies/<int:mince_pie_id>', views.detail, name='detail'),
    path('mince-pies/<int:mince_pie_id>/review/', views.review, name='review'),
]
