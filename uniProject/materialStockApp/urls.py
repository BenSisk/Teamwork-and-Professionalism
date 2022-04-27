from django.urls import include, path
from . import views


urlpatterns = [
    path('stock/', views.StockManagementView, name='materialStockApp'),
    path('addItems/', views.addItemsView, name='addItems'),
    path('updateItems/<str:pk>/', views.updateItemsView, name='updateItems'),
    path('deleteItems/<str:pk>/', views.deleteItemsView, name="deleteItems"),
]