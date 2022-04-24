from django.contrib import admin
from .forms import StockCreateForm

# Register your models here.
from .models import Stock

class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['name', 'materialType', 'quantity']
    form = StockCreateForm

admin.site.register(Stock, StockCreateAdmin)
