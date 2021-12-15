# Project SeeSky - satelite tracker
A simple web application for tracking passing satellites over a selected point writen in python.
Informations are granted in two ways. From web interface and by email newsletter.

## Table of Contents
- General info
- Technologies
- Setup

## General info
App was created in learning process of python language. The task was to use as many elements of the python language as possible:
- API
- Framework Django
- few built in libraries, and functionalities such (math, datetime e.t.c)
- few additional libraries (pytz, sscws, suntime, e.t.c)
- Periodic and scheduled task menager (celery library with redis server)
- database (sqlite supported with ORM built in into Django)
- frontend created using jinja (Html with CSS, python)

## Technologies
- Python 3.9 witch additional libraries(requirements.txt):
- Django
- HTML 
- CSS (mostly Bootstrap 5) 


## Setup
To run this project:
*instal locally all required libraries (all in requirements.txt file)
*provide the variables for smtp email serwer, redis serwer, celery (all variables ar in seesky/settings.py path)
#### email settings
  EMAIL_HOST = EMAIL_SERVER
  EMAIL_PORT = EMAIL_PORT
  EMAIL_HOST_USER = EMAIL_LOGIN
  EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
  EMAIL_USE_SSL = EMAIL_SSL (True/False)
  EMAIL_USE_TLS = EMAIL_TLS (True/False)
  (only one can by True!)
#### celery/redis settings
CELERY_BROKER_URL = e.g.('redis://localhost:6379')
CELERY_TIMEZONE = e.g.('Europe/Warsaw')
if run without debug mode !!
ALLOWED_HOSTS = []


