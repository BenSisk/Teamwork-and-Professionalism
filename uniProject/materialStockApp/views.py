from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Stock
from .forms import StockCreateForm, StockUpdateForm

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
        return redirect('/stock')

    context = {
        "form": form,
        "title": "Add Item",
    }

    return render(request, "addItems.html", context)

@login_required
def updateItemsView(request, pk):
        queryset = Stock.objects.get(id=pk)
        form = StockUpdateForm(instance=queryset)

        if request.method == 'POST':
            form = StockUpdateForm(request.POST, instance=queryset)

            if form.is_valid():
                form.save()
                return redirect('/stock')
            
        context = {'form' : form}

        return render(request, 'addItems.html', context)


@login_required
def deleteItemsView(request, pk):
        queryset = Stock.objects.get(id=pk)
        if request.method == 'POST':
            queryset.delete()
            return redirect('/stock')

        return render(request, 'deleteItems.html')

