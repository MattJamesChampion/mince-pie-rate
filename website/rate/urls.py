from django.urls import path

from . import views

app_name = 'rate'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:mince_pie_id>', views.detail, name='detail'),
]
