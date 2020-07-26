# Memory Map Toolkit

The Memory Map Toolkit is a web application for creating interactive maps for heritage, history, tourism, or any other circumstance in which you want to attach audio, images or text to an interactive map.

It is built and maintained by the Bartlett Centre for Advanced Spatial Analysis and the School of Architecture, University College London.

Sites using the Memory Map Toolkit include the Jewish East End Memory Map, ..., and ....

## Bugs

## Feature Requests


## Requirements

A server capable of running Python 3, Django, PostgreSQL / Postgis, and a web server such as Apache or Nginx to which you have adminstrative access.

## Installation

### Quickstart for Ubuntu 20 Server Edition Using Apache


sudo apt install ...

git clone ...

python -m virtualenv venv/memorymap-toolkit

source venv/memorymap-toolkit

cd memorymap-toolkit/

pip install -r requirements.txt

Create database
Add details to secret_settings.py

python manage.py runserver 0:8000 --settings=

Copy example apache conf
Edit apache conf

Restart apache


#### Extra - SSL

We **highly recommend** that you install an SSL certificate so that traffic to and from your website is encrypted. The easiest way to do this is using LetsEncrypt...






### In detail





## Todo:




- mapHandler.js - probably needs to be refactored as there are things polluting the global namespace

- Move single settings file into base, development, production and secret_settings files

- Example Apache config

- Logging

- Django Analytical

- Uploadable/Changeable logo

- Custom stylesheet

- sitemaps

- Barlett, CASA & UCL logos! Need to be somewhere...