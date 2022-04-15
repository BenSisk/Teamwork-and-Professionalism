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
import base64
from decimal import *

# Static configuration... Will move to a configuration file
ENCODED_API_KEY="ZTcxMTFlZGRlMTY2MDBiZjM4MmFkNDM3ZmM0YjI2OGIwNzc5MTY4ODBkNmE1NjljZjg5NzM4YTExN2RjNDFhYg=="
USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
TMP_DIR = "/tmp/"
TMP_FILE = "tmpPageResults.txt"

getNewPage = False
filteredResults = []
searchURL = "https://serpapi.com/search.json?engine=google&q=###PRODUCT###&location=United+Kingdom&google_domain=google.co.uk&gl=uk&hl=en&tbm=shop&num=100&api_key=###KEY###"
productString="timber+%28L%29+%28T%29+%28W%29"
urlStrip = "https://www.google.co.uk/url?url="

def update_url(url, searchString, API_KEY):
	url = url.replace("###PRODUCT###", searchString)

	# decode key
	apiKey = base64.b64decode(ENCODED_API_KEY).decode('utf-8')

	url = url.replace("###KEY###", apiKey)
	return url

def get_json_results(searchString):
	url = update_url(searchURL, searchString, ENCODED_API_KEY)
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
def calculate_delivery_cost(provider, price):
	if provider == "B&Q" and price < 50:
		delivery = "5.00"
	elif provider == "B&Q" and price >= 50:
		delivery = "0.00"
	elif provider == "Wickes" and price < 75:
		delivery = "5.00"
	elif provider == "Wickes" and price >= 75:
		delivery = "0.00"
	else:
		delivery = "10.00"

	return delivery

def extract_details(jsonFile):
	if exists(jsonFile):
		with open(jsonFile) as jsonContent:
			data = json.load(jsonContent)

		for key in data["shopping_results"]:
			dimensions = get_dimensions(key["title"])

			# get pack size

			# filter out products that don't have the dimensions in the title to avoid headaches
			if dimensions != False:
				packSize = extract_pack_size(key["title"])

				if packSize is not False:
					dimensions.append(packSize)

				volume = calculate_volume(dimensions)
				price = float(key["price"].strip("£"))

				if "delivery" not in key["delivery"]:
					delivery = calculate_delivery_cost(key["source"],price) 
				else:
					try:
						delivery = str(regex.search("(?<=£)(.*)(?=\sdelivery)", key["delivery"]).group())
					except:
						if "Free" in key["delivery"]:
							delivery = "0.00"
						else:
							delivery = key["delivery"]

				# calculate the price per cubic meter including delivery
				price = price + float(delivery)
				costPerVolume = Decimal(price) / Decimal(volume)

				resultList = [key["source"], key["title"], volume, key["price"], delivery, key["link"].replace(urlStrip,""), float(round(costPerVolume, 2))]
				filteredResults.append(resultList)

		sortedList = sorted(filteredResults, key=lambda x: x[6])
		print([item[-1] for item in sortedList])
#		print(sortedList)
		return sortedList
	else:
		print("No json file found, fetching")
		data = get_json_results(productString)
		save_page(data)

def extract_pack_size(title):
	try:
		results = regex.search("(?<=Pack of )[0-9]", title).group()
	except:
		packSize = False
		pass
	else:
		packSize = int(regex.search("[0-9]", results).group())

	return packSize

def get_dimensions(title):
	dimension = []
	try:
		dimension.append(regex.search("\(L\)[^\s]+", title).group())
		dimension.append(regex.search("\(W\)[^\s]+", title).group())
		dimension.append(regex.search("\(T\)[^\s]+", title).group())
	except:
		return False
	else:
		dimensions = strip_dimensions(dimension)
		dimensions = convert_to_mm(dimensions)

		return dimensions

def strip_dimensions(dimensions):
	newDimensions = [s.replace('(L)', '') for s in dimensions]
	newDimensions = [s.replace('(W)', '') for s in newDimensions]
	newDimensions = [s.replace('(T)', '') for s in newDimensions]
	return newDimensions

def convert_to_mm(dimensions):
	for x, item in enumerate(dimensions):
		try:
			results = regex.search("[0-9][Mm](?:^|\s|$)", item).group()
		except:
			# no results, extract the digits
			dimensions[x] = float(regex.search("[+-]?([0-9]*[.])?[0-9]+", item).group())
			pass
		else:
			# extract dimensions which  contain a decimal place
			size = float(regex.search("[+-]?([0-9]*[.])?[0-9]+", item).group())
			dimensions[x] = size

	return dimensions

def calculate_volume(dimensions):
	volume = (dimensions[0] / 1000 ) * ( dimensions[1] / 1000 )* (dimensions[2] / 1000)

	# see if we have a pack size
	if len(dimensions) == 4:
		volume * dimensions[-1]

	# convert to meters from m to get m^3
	return (volume)

# Don't waste all the API calls for now, only get a new page when specified
if ( getNewPage ):
	data = get_json_results("timber")

	if save_page(data):
		print("page saved successfully")

else:
	context = extract_details("data.json")
#	print(context)
