from django.shortcuts import render
import io
import urllib, base64
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
import json
import pandas as pd
import numpy as np
from pandas.plotting import register_matplotlib_converters
from .api_keys import *
from .forms import pricePredictionForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# returns the predicted value from azure for the given material and date (m-Y)
def queryAzure(date, material, model):
	data = {
		"Inputs": {
			"data":
			[
				{
					"Date": date
				},
			]
		},
		"GlobalParameters": {
			"quantiles": [0.025,0.975]
		}
	}

	body = str.encode(json.dumps(data))

	# Static IP of the Azure Endpoints
	endpoint = material + "-" + model
	url = "http://" + ipaddress[model] + ":80/api/v1/service/" + endpoint + "/score"

	# API keys are read from a dictionary in a separate python file named apikeys
	api_key = apikeys[endpoint] # Replace this with the API key for the web service
	
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

	req = urllib.request.Request(url, body, headers)

	try:
		response = urllib.request.urlopen(req)

		result = response.read()
		result = json.loads(result.decode('utf-8'))
		result = round(int(result["Results"]["forecast"][0]))
	except urllib.error.HTTPError as error:
		print("The request failed with status code: " + str(error.code))
		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())
		print(error.read().decode("utf8", 'ignore'))
		return -1

	return result

def getGraph(data, timeframe, material, model):
	register_matplotlib_converters()
	timeSplit = timeframe.split("-")
	newDate = timeSplit[1] + "/" + timeSplit[0]

	data.iloc[:, 0] = [ dt.strptime(str(d), '%m/%Y').date() for d in data.iloc[:, 0] ]

	# if query fails and triggers the except block, failedQuery is true and the graph is not plotted
	failedQuery = False

	# next = queryAzure(timeframe, material, model)
	next = 120
	
	if (next == -1):
		failedQuery = True

	x = [data.iloc[len(data) - 1, 0], dt.strptime(newDate, '%m/%Y').date()]
	y = [data.iloc[len(data) - 1, 1], next]

	fig, ax = plt.subplots()
	

	plt.title(material[0].upper() + material[1:] + " Price")

	# graph is plotted if the query was successful, otherwise is an empty graph
	if (not failedQuery):
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
		ax.plot(data.iloc[:, 0], data.iloc[:, 1], color="blue", label="Previous")
		ax.plot(x, y, color="red", label="Predicted")
		ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)

	plt.xlabel("Date")
	plt.ylabel("Price Index")
	plt.grid()
	plt.minorticks_on()
	plt.grid(b=True, which='major',alpha=0.5)
	plt.grid(b=True, which='minor', alpha=0.2)

	# matplotlib graph converted to png and parsed
	buf = io.BytesIO()
	# DPI adjusts what is effectively the resolution of the image
	# however the image size itself is controlled via the template
	fig.savefig(buf,format="png", dpi=250)
	buf.seek(0)
	string=base64.b64encode(buf.read())
	return urllib.parse.quote(string)

@login_required
def prediction(request):
	if request.method == 'POST':
		form = pricePredictionForm(request.POST)
		if form.is_valid():
			material = form.clean_material_data()
			dateTimeframe = form.clean_date_data()
			model = form.clean_model_data()
	else:
		# default if no POST request
		material = "plywood"
		dateTimeframe = 1
		model = "votingensemble"

	currentYear = dt.now().year
	currentMonth = dt.now().month + dateTimeframe
	while (currentMonth > 12):
		currentMonth -= 12
		currentYear += 1

	# concatenate into format Azure is expecting
	date = str(currentYear) + "-" + str(currentMonth)

	# read corresponding previous data to be displayed
	dataset_test = pd.read_csv("data/" + material + ".csv")

	# get image of the matplotlib graph to be displayed
	uri = getGraph(dataset_test, date, material, model)

	# direct to prediction template, with the  matplotlib graph image
	# and entry form parameters for submitting data (material type and prediction timeframe)
	return render(request, 'prediction.html', {"data": uri, "form" : pricePredictionForm})