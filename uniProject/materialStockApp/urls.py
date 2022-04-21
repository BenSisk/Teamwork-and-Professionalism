from django.urls import include, path
from . import views


urlpatterns = [
    path('stock/', views.StockManagementView, name='materialStockApp'),
    path('addItems/', views.addItemsView, name='addItems'),
]