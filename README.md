# Memory Map Toolkit

The Memory Map Toolkit is a web application for creating interactive maps for heritage, history, tourism, or any other circumstance in which you want to attach audio, images or text to an interactive map.

It is built and maintained by the Bartlett Centre for Advanced Spatial Analysis and the School of Architecture, University College London.



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

- Example Apache config

- Barlett, CASA & UCL logos! Need to be somewhere... 

- License

- Favicon




## Copyright

Copyright (C) 2020  Duncan Hay / University College London

d.hay@ucl.ac.uk

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

