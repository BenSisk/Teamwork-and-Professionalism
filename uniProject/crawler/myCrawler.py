#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 10:23:52 2022

@author: Anthony Donnelly
"""
from urllib.request import urlopen
import re as regex
import json
from os import remove
import base64
from decimal import *
from os.path import exists
import string

# Static configuration... Will move to a configuration file
ENCODED_API_KEY = "ZTcxMTFlZGRlMTY2MDBiZjM4MmFkNDM3ZmM0YjI2OGIwNzc5MTY4ODBkNmE1NjljZjg5NzM4YTExN2RjNDFhYg=="
USER_AGENT = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
TMP_DIR = "/tmp/"
TMP_FILE = "tmpPageResults.txt"

BLACKLIST_FILE = "data/blacklist.txt"

getNewPage = False
searchURL = "https://serpapi.com/search.json?engine=google&q=###PRODUCT###&location=United+Kingdom&google_domain=google.co.uk&gl=uk&hl=en&tbm=shop&num=100&api_key=###KEY###"
productString = "+%28L%29+%28T%29+%28W%29"
urlStrip = "https://"


def update_url(url, searchString):
    url = url.replace("###PRODUCT###", searchString)

    # decode key
    apiKey = base64.b64decode(ENCODED_API_KEY).decode('utf-8')

    url = url.replace("###KEY###", apiKey)
    return url


def get_json_results(searchString):
    url = update_url(searchURL, searchString)
    response = urlopen(url)

    buf = response.read()
    dataJson = json.loads(buf.decode('utf-8'))

    return dataJson


def save_page(jsonData):
    try:
        if exists("data/data.json"):
            remove("data/data.json")

        with open('data/data.json', 'w', encoding='utf-8') as f:
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
        delivery = "Collection Only"

    return delivery


# Work out delivery costs, very limited check at the minute
def get_delivery(key, price):
    if "delivery" not in key["delivery"]:
        delivery = calculate_delivery_cost(key["source"], price)
    else:
        try:
            delivery = str(regex.search("(?<=£)(.*)(?=\sdelivery)", key["delivery"]).group())
        except AttributeError:
            if "Free" in key["delivery"]:
                delivery = "0.00"
            else:
                delivery = key["delivery"]

    return delivery


def extract_details(jsonFile, calcVolume):
    if exists(jsonFile):
        filteredResults = []
        dimensions = False

        with open(jsonFile) as jsonContent:
            data = json.load(jsonContent)

        for key in data["shopping_results"]:
            if calcVolume:
                dimensions = get_dimensions(key["title"])

            # get pack size

            # filter out products that don't have the dimensions in the title to avoid headaches
            if dimensions is not False and calcVolume:
                packSize = extract_pack_size(key["title"])

                if packSize is not False:
                    dimensions.append(packSize)

                volume = calculate_volume(dimensions)
                price = float(key["price"].strip("£"))

                delivery = get_delivery(key, price)

                # calculate the price per cubic meter including delivery
                try:
                    price = price + float(delivery)
                    delivery = "£" + delivery
                except ValueError:
                    # no delivery cost
                    pass

                if len(dimensions) == 4:
                    costPerVolume = (Decimal(price) / dimensions[-1]) / Decimal(volume)
                else:
                    costPerVolume = Decimal(price) / Decimal(volume)

                # key["link"].replace(urlStrip,"")
                resultList = [key["thumbnail"], key["title"], volume, key["price"], delivery, key["link"],
                              '{0:,.2f}'.format(float(round(costPerVolume, 2)))]

                # only add if it's not in a blacklist
                if not blackListed(key["link"]):
                    filteredResults.append(resultList)

            elif not calcVolume:
                volume = "0"
                price = key["price"].strip("£")
                price = float(price.replace(',', ''))
                delivery = get_delivery(key, price)
                resultList = [key["thumbnail"], key["title"], volume, key["price"], delivery, key["link"]]

                if not blackListed(key["link"]):
                    filteredResults.append(resultList)

        if calcVolume:
            # sort on volume
            sortedList = sorted(filteredResults, key=lambda x: x[6])
        else:
            # sort on price
            sortedList = sorted(filteredResults, key=lambda x: x[3])

        return sortedList
    else:
        print("No json file found, fetching")
        data = get_json_results(productString)
        save_page(data)


def extract_pack_size(title):
    try:
        results = regex.search("(?<=pack of )[0-9]", title.lower()).group()
    except AttributeError:
        packSize = False
        pass
    else:
        packSize = int(regex.search("[0-9]", results).group())

    return packSize


def get_dimensions(title):
    dimension = []
    try:
        dimension.append(regex.search('\(l\)[^\s]+', title.lower()).group())
        dimension.append(regex.search('\(w\)[^\s]+', title.lower()).group())
        dimension.append(regex.search('\(t\)[^\s]+', title.lower()).group())
    except AttributeError:
        return False
    else:
        dimensions = strip_dimensions(dimension)
        dimensions = convert_to_mm(dimensions)

        return dimensions


def strip_dimensions(dimensions):
    newDimensions = [s.replace('(L)', '') for s in dimensions]
    newDimensions = [s.replace('(W)', '') for s in newDimensions]
    newDimensions = [s.replace('(T)', '') for s in newDimensions]
    newDimensions = [s.replace('(l)', '') for s in newDimensions]
    newDimensions = [s.replace('(w)', '') for s in newDimensions]
    newDimensions = [s.replace('(t)', '') for s in newDimensions]

    return newDimensions


def convert_to_mm(dimensions):
    for x, item in enumerate(dimensions):
        try:
            results = regex.search("[0-9][Mm](?:^|\s|$)", item).group()
        except AttributeError:
            # no results, extract the digits
            try:
                    dimensions[x] = float(regex.search("[+-]?([0-9]*[.])?[0-9]+", item).group())
            except AttributeError:
                    # return default dimensions of 0
                    dimensions[x] = 0
        else:
            # extract dimensions which  contain a decimal place
            size = float(regex.search("[+-]?([0-9]*[.])?[0-9]+", item).group())
            # convert to mm
            dimensions[x] = size * 1000

    return dimensions


def calculate_volume(dimensions):
	try:
		volume = (int(dimensions[0]) / 25.4) * (int(dimensions[1]) / 25.4) * (int(dimensions[2]) / 25.4)
	except ValueError:
		# return volume of 0
		volume = 0

	return float(volume)

def parseSearchString(search):
	if search is None:
		search = "timber"

	if search is "":
		search = "timber"

	search = str(search)

	pattern = r'[' + string.punctuation + ']'

	# Remove special characters from the string
	search = regex.sub(pattern, '', search)

	return search


def isBool(input):
	if input is not type(True):
		input = False

	return input

def isInt(input):
	try:
		input = int(input)
	except ValueError:
		input = -1

	return input

# Don't waste all the API calls for now, only get a new page when specified
def startCrawler(getNewPage, numResults, searchString, volume):
    searchString = parseSearchString(searchString)
    getNewPage = isBool(getNewPage)
    numResults = isInt(numResults)

    if getNewPage:
        if volume:
            searchString = searchString + "+%28L%29+%28T%29+%28W%29"

        data = get_json_results(searchString)

        if save_page(data):
            print("page saved successfully")

    results = extract_details("data/data.json", volume)

    # ensure we don't go out of bounds
    if numResults > len(results):
        return results
    else:
        return results[:numResults]


def strip_website(link):
    linkNew = link.replace('https://www.google.co.uk/url?url=', "")
    linkNew = linkNew.replace('https://', "")
    linkNew = linkNew.replace('http://', "")

    link = regex.sub("(?:\/([a-zA-Z0-9].*))", "", linkNew)

    return link


def get_website_list():
    website_list = []
    try:
        with open("data/data.json") as jsonContent:
            data = json.load(jsonContent)
    except FileNotFoundError:
        return ""

    else:
        for key in data["shopping_results"]:
            link = key["link"]

            link = strip_website(link)

            if link not in website_list and len(link) > 0:
                website_list.append(link)

        return website_list


def add_to_blackList(site):
    if not exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "w") as blacklistFile:
            blacklistFile.write(site + "\n")
    else:
        with open(BLACKLIST_FILE) as f:
            if site not in f.read():
                with open(BLACKLIST_FILE, "a") as blacklistFile:
                    blacklistFile.write(site + "\n")


def remove_from_blacklist(site):
    import os
    tmpFile = "data/blacklist.new"

    print("to be delete " + site)
    with open(BLACKLIST_FILE) as f, open(tmpFile, "w") as fout:
        for line in f:
            print("Current line is: " + line)
            if line == site + "\n":
                print("found match")
                line = line.replace(site + "\n", "")

            fout.write(line)

    os.rename(tmpFile, BLACKLIST_FILE)


def get_blacklist():
    with open(BLACKLIST_FILE) as file:
        website = [line.rstrip() for line in file]

    return website


def blackListed(link):
    link = strip_website(link)
    if exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE) as f:
            if link in f.read():
                return True
    else:
        return False
