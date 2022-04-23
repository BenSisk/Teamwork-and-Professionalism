from django.urls import include, path
from . import views


urlpatterns = [
 path('search/', views.crawler_view, name='crawler'),
 path('blacklist/', views.blacklist, name="blacklist"),
]
