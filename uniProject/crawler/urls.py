from django.urls import include, path
from . import views


urlpatterns = [
 path('crawler/', views.crawler_view, name='crawler'),
]
