from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import myCrawler

# Create your views here.
@login_required

def crawler_view(request):
	results = myCrawler.extract_details("data.json")
	return render(request, 'crawler.html', {'results': results})
