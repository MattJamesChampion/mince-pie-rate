from django.urls import path, include
from django.views.generic.base import ContextMixin
from allauth.account import views as auth_views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

class LogoutViewWithContext(ContextMixin, auth_views.LogoutView):
    pass

urlpatterns = [
    path('', views.index, name='index'),
    path('mince-pies/', views.overview, name='overview'),
    path('mince-pies/<int:mince_pie_id>', views.detail, name='detail'),
    path('mince-pies/<int:mince_pie_id>/review/submit', views.submit_review, name='submit_review'),
    path('mince-pies/add/', views.add_mince_pie, name='add_mince_pie'),
    path('accounts/login/', auth_views.LoginView.as_view(extra_context={'active_page' : 'login',}), name='account_login'),
    path('accounts/logout/', LogoutViewWithContext.as_view(extra_context={'active_page' : 'logout',}), name='account_logout'),
    path('accounts/signup/', auth_views.SignupView.as_view(extra_context={'active_page' : 'signup',}), name='account_signup'),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
