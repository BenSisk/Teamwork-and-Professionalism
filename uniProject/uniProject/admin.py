from django.shortcuts import render
from django import forms

class InputForm(forms.Form):
   
    username = forms.CharField(max_length = 50)
    password = forms.CharField(widget = forms.PasswordInput())

def admin(request):
    """View function for home page of site."""
    context ={}
    context['form']= InputForm()
    #if not request.user.is_authenticated:
        #return render(request, 'index.html')
    #else:
        # Render the HTML template index.html with the data in the context variable
    return render(request, 'admin.html', context)

