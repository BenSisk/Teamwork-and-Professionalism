#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 10:23:52 2022

@author: Anthony Donnelly
"""
from urllib.request import urlopen
import re as regex
import json
from os.path import exists

# Static configuration... Will move to a configuration file
API_KEY = "e7111edde16600bf382ad437fc4b268b077916880d6a569cf89738a117dc41ab"
USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
TMP_DIR = "/tmp/"
TMP_FILE = "tmpPageResults.txt"

getNewPage = False
filteredResults = []
searchURL = "https://serpapi.com/search.json?engine=google&q=###PRODUCT###&location=United+Kingdom&google_domain=google.co.uk&gl=uk&hl=en&tbm=shop&num=100&api_key=###KEY###"
productString="timber+%28L%29+%28T%29+%28W%29"


def update_url(url, searchString, API_KEY):
	url = url.replace("###PRODUCT###", searchString)
	url = url.replace("###KEY###", API_KEY)

	print(url)
	return url

def get_json_results(searchString):
	url = update_url(searchURL, searchString, API_KEY)
	response = urlopen(url)

	buf = response.read()
	dataJson = json.loads(buf.decode('utf-8'))

	return dataJson

def save_page(jsonData):
	try:
		with open('data.json', 'w', encoding='utf-8') as f:
			json.dump(jsonData, f, ensure_ascii=False, indent=4)
		return True
	except OSError:
		return False

def extract_details(jsonFile):
	if exists(jsonFile):
		with open(jsonFile) as jsonContent:
			data = json.load(jsonContent)

		for key in data["shopping_results"]:
#			dimensions = get_dimensions(key["title"])

			resultList = [key["source"], key["title"], key["price"], key["delivery"], key["link"]]
			filteredResults.append(resultList)


		return filteredResults
	else:
		print("No json file found, fetching")
		data = get_json_results(productString)
		save_page(data)


#def get_dimensions(title):

# Don't waste all the API calls for now, only get a new page when specified
#if ( getNewPage ):
#	data = get_json_results("timber")
#
#	if save_page(data):
#		print("page saved successfully")
#
#else:
#	context = extract_details("data.json")
