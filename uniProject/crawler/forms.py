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


def update_website_list():
    black_list_website = [(x, x) for x in myCrawler.get_website_list()]

    return black_list_website


def update_blacklist():
    current_black_list_website = [(x, x) for x in myCrawler.get_blacklist()]

    return current_black_list_website


def string_to_bool(data):
    if data == "True":
        return True
    else:
        return False


class currentBlackList(forms.Form):
    def __init__(self, *args, **kwargs):
        super(currentBlackList, self).__init__(*args, **kwargs)
        current_black_list_website = update_blacklist()
        self.fields['removeList'].choices = current_black_list_website

    removeList = forms.TypedChoiceField(label="Current items in blacklist", widget=forms.Select(), initial='')


class BlackList(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BlackList, self).__init__(*args, **kwargs)
        black_list_website = update_website_list()
        self.fields['webBlackList'].choices = black_list_website

    webBlackList = forms.TypedChoiceField(label='BlackList',
                                          widget=forms.Select(), initial='')


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
