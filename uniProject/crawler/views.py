from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import myCrawler
from .forms import SearchCriteria, BlackList, currentBlackList


# Create your views here.
@login_required
def blacklist(request):
    if request.method == 'POST':
        website = request.POST.get('webBlackList', '')
        delete = request.POST.get('removeList', '')

        if len(website) > 0:
            myCrawler.add_to_blackList(website)
            message = "Added {} to blacklist".format(website)

        if len(delete) > 0:
            myCrawler.remove_from_blacklist(delete)
            message = "deleted {} from blacklist".format(delete)

        blackListForm = currentBlackList()

        # in the event we don't send a post request and message is unset. i.e accessing
        # /blacklist/ with a get request
        try:
            message
        except NameError:
            message = "No item to delete"

        context = {
            'message': message,
            'blacklistForm': blackListForm,
        }

    else:
        blackListForm = currentBlackList()

        context = {
            'blacklistForm': blackListForm,
        }

    return render(request, 'blacklist.html', context)


@login_required
def crawler_view(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchCriteria(request.POST)
        blackListForm = BlackList()

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            searchString = form.modify_search_query()
            newPage = form.get_new_page()
            numResults = form.get_results()
            volume = form.get_volume()

            results = myCrawler.startCrawler(newPage, numResults, searchString, volume)

            context = {
                'forms': True,
                'form': form,
                'blacklistForm': blackListForm,
                'results': results,
                'volume': volume,
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
