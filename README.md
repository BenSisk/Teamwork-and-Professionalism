## Teamwork and Professionalism Assignment
A website build using the django framework for the assignment in module KV6002. Using a mixture of python, html and css

Table of contents
=================

<!--ts-->
   * [Installation](#Installation)
   * [Setup](#Setup)
      * [Database](#Database)
      * [Superuser](#Superuser)
   * [Tests](#Tests)
   * [Dependency](#Dependency)
   * [Starting Server](#Server)
<!--te-->

## Installation

```
pip install -r requirements.txt
```

## Database

```
python3 manage.py makemigration
python3 manage.py migrate
```

## Superuser
```
python3 manage.py createsuperuser
```

## Test
```
python3 manage.py test -v 2
```

## Server

```
python3 manage.py test -v 2
```
The server will now be available on http://127.0.0.1:80


