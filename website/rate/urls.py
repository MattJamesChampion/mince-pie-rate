from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mince-pies/', views.overview, name='overview'),
    path('mince-pies/<int:mince_pie_id>', views.detail, name='detail'),
    path('mince-pies/<int:mince_pie_id>/review/submit', views.submit_review, name='submit_review'),
    path('mince-pies/add/', views.add_mince_pie, name='add_mince_pie'),
    path('account/login/', auth_views.LoginView.as_view(extra_context={'active_page' : 'login',}), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
