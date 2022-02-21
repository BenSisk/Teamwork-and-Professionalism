#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 10:23:52 2022

@author: Anthony Donnelly
"""
import urllib3 as r
import re as regex
import subprocess

#SEARCH_URL = "https://duckduckgo.com/?q=###PRODUCT###&t=h_&iax=shopping&ia=shopping"
SEARCH_URL = "https://www.google.co.uk/search?q=###PRODUCT###&tbm=shop&gl=gb&start=###page###"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
TMP_DIR = "/tmp/"
TMP_FILE = "tmpPageResults.txt"
PAGE_INCREMENT = 60

def page_cleanup(filename):
        # pointless doing this in python when tools exists to handle it already in
        # one line of code
	subprocess.call(["sed -i -e '/class=/d' {}".format(filename)], shell=True)
	subprocess.call(["sed -i -e '/div/d' {}".format(filename)], shell=True)

def get_page_results(searchString):
	newString = ""
	start_page = 0

	# first 10 pages, 60 per page = 600
	while start_page < 60:
		url = SEARCH_URL.replace("###PRODUCT###", searchString)
		url = url.replace("###PAGE###", str(start_page))

		http = r.PoolManager()
		page = http.request("GET", url)

		page = (page.data).decode('latin-1')

		for element in range(0, len(page)):
			newString += page[element]
			if page[element] == ">":
				newString += "\n"

		save_page(newString)

		start_page += PAGE_INCREMENT

def save_page(page):
	## todo
	## save all to one file
	## check if file already exists
	## remove file on cleanup
        with open(TMP_FILE, 'a') as file:
                file.write(page)

        #page_cleanup(TMP_FILE)


def extract_price(TMP_FILE):
        print("Not done")


def extract_details():
	file = open(TMP_FILE, 'r')
	lines = file.readlines()

	for line in lines:
		if line.startswith('£'):# and "span" in line:
			print(line)

get_page_results("timber")

extract_details()
