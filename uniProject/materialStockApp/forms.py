from unicodedata import category
from django import forms
from django.shortcuts import redirect, render
from .models import Stock

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'materialType', 'quantity']

        def cleanDataName(self):
            name = self.cleaned_data.get('name')
            if not name:
                raise forms.ValidationError('This is as required field')
            return name

        def cleanDataMaterialType(self):
            material = self.cleaned_data.get('materialType')
            if not material:
                raise forms.ValidationError('This is as required field')

            return material

        def cleanDataQuantity(self):
            quantity = self.cleaned_data.get('quantity')
            if not quantity:
                raise forms.ValidationError('This is as required field')
            return 
            
class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'materialType', 'quantity']

    
