from django.shortcuts import render
import io
import urllib, base64
import matplotlib.pyplot as plt
from datetime import datetime
import json

# Create your views here.

def prediction(request):
	currentMonth = datetime.now().month + 1
	currentYear = datetime.now().year
	while (currentMonth > 12):
		currentMonth -= 12
		currentYear += 1

	date = str(currentYear) + "-" + str(currentMonth)

	# Request data goes here
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

	url = 'http://20.108.92.23:80/api/v1/service/plywood-votingensemble/score'
	api_key = 'API KEY GOES HERE' # Replace this with the API key for the web service
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

	req = urllib.request.Request(url, body, headers)

	try:
		response = urllib.request.urlopen(req)

		result = response.read()
	except urllib.error.HTTPError as error:
		print("The request failed with status code: " + str(error.code))

		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())
		print(error.read().decode("utf8", 'ignore'))

	
	result = json.loads(result.decode('utf-8'))
	result = round(int(result["Results"]["forecast"][0]))

	plt.plot(range(10))
	fig = plt.gcf()

	buf = io.BytesIO()
	fig.savefig(buf,format="png")
	buf.seek(0)
	string=base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)


	return render(request, 'prediction.html', {"data":uri, "oof": result})
