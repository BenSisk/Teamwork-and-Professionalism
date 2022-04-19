from django import forms

NEW_PAGE = [
    (True, "Yes"),
    (False, "No"),
    ]

class SearchCriteria(forms.Form):
	searchTerm = forms.CharField(help_text="Material to search for")

	newPage = forms.CharField(label="Fetch New Page:", widget=forms.Select(choices=NEW_PAGE))


	def modify_search_query(self):
		data = self.cleaned_data['searchTerm']

		# replace spaces with url encode

		data = data.replace(" ", "%20")
		# add in dimensions into  search
		searchString = data + "+%28L%29+%28T%29+%28W%29"

		return searchString

	def get_new_page(self):
		data = self.string_to_bool(self.cleaned_data['newPage'])

		print(data)
		# no is boolean?
		if type(data) == type(True):
			return data
		else:
			return False


	def string_to_bool(self, data):
		if data == "True":
			return True
		else:
			return False
