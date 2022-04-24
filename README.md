## Teamwork and Professionalism Assignment
A website build using the django framework for the assignment in module KV6002. Using a mixture of python, html and css

Table of contents
=================

<!--ts-->
   * [Installation](#Installation)
      * [Database](#Database)
      * [Superuser](#Superuser)
   * [Tests](#Tests)
   * [Dependency](#Dependency)
   * [Starting Server](#Server)
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


