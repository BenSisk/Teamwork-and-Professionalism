from django.urls import include, path
from . import views
from .forms import UserLoginForm


urlpatterns = [
 path('', views.index, name="index"),
 path('login/', views.Login.as_view(template_name='login.html', authentication_form=UserLoginForm), name='login'),
 path('logout/', views.logout_view, name='logout'),
 path('admintest/', views.admin_view, name='admin'),
]
