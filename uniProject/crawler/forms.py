from django import forms
from . import myCrawler

NEW_PAGE = [
    (True, "Yes"),
    (False, "No"),
]

RESULTS_PER_PAGE = [
    (25, "25"),
    (50, "50"),
    (75, "75"),
    (100, "100"),
]

BLACK_LIST_WEBSITE = [(x, x) for x in myCrawler.get_website_list()]

def string_to_bool(data):
    if data == "True":
        return True
    else:
        return False


class BlackList(forms.Form):
    webBlackList = forms.CharField(label="Add to Blacklist", widget=forms.Select(choices=BLACK_LIST_WEBSITE))

    def get_website(self):
        data = self.cleaned_data("webBlackList")

        return data

class SearchCriteria(forms.Form):
    searchTerm = forms.CharField(label="Search:")

    newPage = forms.CharField(label="New Page:", widget=forms.Select(choices=NEW_PAGE))
    searchResults = forms.CharField(label="Results:", widget=forms.Select(choices=RESULTS_PER_PAGE))
    calcVolume = forms.CharField(label="Calculate Volume:", widget=forms.Select(choices=NEW_PAGE))

    def modify_search_query(self):
        data = self.cleaned_data['searchTerm']

        # replace spaces with url encode

        data = data.replace(" ", "%20")
        # add in dimensions into  search
        searchString = data

        return searchString

    def get_new_page(self):
        data = string_to_bool(self.cleaned_data['newPage'])

        if isinstance(data, bool):
            return data
        else:
            return False

    def get_volume(self):
        data = string_to_bool(self.cleaned_data['calcVolume'])

        if isinstance(data, bool):
            return data
        else:
            return False

    def get_results(self):
        data = self.cleaned_data['searchResults']

        return int(data)
