from django.urls import path
from . import views
from .forms import UserLoginForm


urlpatterns = [
 path('', views.index, name="index"),
 path('login/', views.Login.as_view(template_name='login.html', authentication_form=UserLoginForm), name='login'),
 path('logout/', views.logout_view, name='logout'),
 path('admin/', views.admin_view, name='admin'),
 path('upload/', views.upload_view, name='upload'),
 path('account/', views.account_view, name='account'),
 path('products/', views.display_view, name='display')
]
