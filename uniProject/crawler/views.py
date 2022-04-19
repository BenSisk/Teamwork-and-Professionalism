from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import myCrawler
from .forms import SearchCriteria

# Create your views here.

def crawler_view(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchCriteria(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            searchString = form.modify_search_query()
            newPage = form.get_new_page()

            results = myCrawler.startCrawler(newPage, searchString)

            context = {
               'forms': True,
               'form': form,
               'results': results
            }

    # If this is a GET (or any other method) create the default form.
    else:
        searchString = "Timber"
        form = SearchCriteria(initial={'searchTerm': searchString})

        context = {
            'forms': True,
            'form': form,
        }

    return render(request, 'crawler.html', context)
