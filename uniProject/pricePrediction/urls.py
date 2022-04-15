from django.urls import include, path
from . import views


urlpatterns = [
 path('pricePrediction/', views.prediction, name='pricePrediction'),
]
