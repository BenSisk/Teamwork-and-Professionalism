from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import *
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required


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