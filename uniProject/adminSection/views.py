import os.path

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import *
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Document
from .forms import DocumentForm

def index(request):
    return render(request, 'index.html')

class Login(LoginView):
 template_name = 'login.html'

def logout_view(request):
 logout(request)
 return redirect('/')

@login_required
def admin_view(request):
 return render(request, 'admin.html')

@login_required
def upload_view(request):
#    print(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'Select a image to upload!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            newdoc = Document(title = form.cleaned_data['title'], desc = form.cleaned_data['desc'], docfile=request.FILES['docfile'])
            x = str(request.FILES['docfile'])
            x = x.split('.')
            extentions = ['jpeg', 'jpg', 'tif', 'png']
            if x[1] in extentions:
                newdoc.save()
                return redirect('upload')
            else:
                message = 'invalid file type, please use a image file!\n'

        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'upload.html', context)

def display_view(request):
 if request.method == 'GET':
        img = Document.objects.all()
        return render(request, 'product.html', {'newdoc': img})

@login_required
def account_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'account.html', {'form': form, 'added': True})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account.html', {'form': form, 'added': False})
