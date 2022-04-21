from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Stock
from .forms import StockCreateForm

# Create your views here.

@login_required
def StockManagementView(request):
    queryset = Stock.objects.all()
    context = {
        "queryset": queryset, 
    }
    return render(request, 'stockManagement.html', context)


@login_required
def addItemsView(request):
    form = StockCreateForm(request.POST or None)
    
    if form.is_valid():
        form.save()

    context = {
        "form": form,
        "title": "Add Item",
    }

    return render(request, "addItems.html", context)