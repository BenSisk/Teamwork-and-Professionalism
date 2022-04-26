## Teamwork and Professionalism Assignment
A website built using the django framework for the assignment in module KV6002. Using a mixture of python, html and css

Table of contents
=================

<!--ts-->
   * [Installation](#Installation)
      * [Database](#Database)
      * [Superuser](#Superuser)
   * [Tests](#Tests)
   * [Dependency](#Dependency)
   * [Starting Server](#Server)
   * [Project Apps](#apps)
      * [Crawler](#crawler)
      * [Admin](#admin)
      * [Price Prediction](#priceprediction)
      * [Stock Management](#stock)
      * [Showcase](#showcase)
<!--te-->

## Installation
You can in stall the requirements with pip, or have your IDE

```
pip install -r requirements.txt
```

### Database

Let django create the database and the necessary tables
```
python3 manage.py makemigration
python3 manage.py migrate
```

### Superuser

The created user will be used to access the admin panel
```
python3 manage.py createsuperuser
```

## Test
Optionally run the test suite
```
python3 manage.py test -v 2
```

## Server

```
python3 manage.py runserver 0.0.0.0:80
```
The server will now be available on http://127.0.0.1:80

## Apps
This project consists of multiple apps each developed by a member of the team.

### Crawler
This app focuses on extracting search data from Google shopping using an api, and parsing the returned json data. Calculations are performed on the returned 
materials such as calculating the volume (cost per cubic inch) of the material, and return the best value for money material.

Other parameters can be tuned on the crawler, such as disabling fetching a new page each search to save on API calls, or filtering the number of returned results. The results returned are sorted by the cheapest material to the most expensive. Other items can be search for such as tools, but calculate volume should be disabled.

The ability to blacklist websites from the search result is also implimented within the crawler, saving the blacklisted sites in a basic text file, with robust error checking on the file, items can also be removed from the list.

### PricePrediction
The price prediction system uses several deep learning algorithms via Microsoft Azure to provide powerful machine learning predicitons based on the price index of various materials. The price prediction has three configurable parameters: Material, Model, and Timescale. The material and model parameters are used to select which model is queried, and the timescale is used within the query to get a prediction of the price at that date. Two model architectures are available: ElasticNet and Voting Ensemble, however, more could be added easily by creating new web service endpoints with some small code modifications.
