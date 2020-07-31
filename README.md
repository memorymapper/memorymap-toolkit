# Memory Map Toolkit

The Memory Map Toolkit is a web application for creating interactive maps for heritage, history, tourism, or any other circumstance in which you want to attach audio, images, text or video to an interactive web map.

It is built and maintained by Duncan Hay at the Bartlett Centre for Advanced Spatial Analysis and the School of Architecture, University College London.


## Features

- Fully-featured content management system built using Django
- Advanced web mapping built with MapboxGL
- Customisable map styles
- Support for multiple basemaps, including Mapbox, Maptiler Cloud, and self-hosted raster and vector tiles
- Responsive design for mobile, tablet, and desktop use


## Installation

We are unable to offer comprehensive installation for all platforms. However, below is a quickstart guide for Ubuntu 20.04 Server Edition using Apache.

### Prerequisites

- A server capable of running Python 3, Django, PostgreSQL / Postgis, and Apache or Nginx to which you have adminstrative access. We've had good experiences using DigitalOcean https://www.digitalocean.com/.

- A domain name that you want to use for your map and some experience of using DNS records.

- Some experience of using the linux command line, logging in to a server using SSH, and familiarity with installing packages and editing configuration files.

- To use the default map style, you need to sign up for a free account with MapTiler Cloud https://www.maptiler.com/cloud/.

### 0. Inititial Server Setup

Follow the instructions for intial server setup here: https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04

Once done, you should have SSH access to your server and have enabled Ubuntu's built-in firewall.

### 1. Install the Required Packages

```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib postgis python3-dev libpq-dev memcached apache2 libapache2-mod-wsgi-py3
```

### 2. Create a New Python Environment

```bash
mkdir venv
python -m venv venv/memorymap-toolkit
source venv/memorymap-toolkit/bin/activate
```

### 3. Download the Memory Map Toolkit and Install the Required Python Libraries
```bash
git clone https://github.com/memorymapper/memorymap-toolkit.git
cd memorymap-toolkit
pip install -r requirements.txt
```

### 4. Configure the Database
```bash
sudo -u postgres psql
```
```sql
CREATE USER memorymappper WITH PASSWORD 'your_password';
CREATE DATABASE memorymap;
GRANT ALL PRIVILEGES ON DATABASE memorymap TO USER memorymapper;
\c memorymap;
CREATE EXTENSION postgis;
\q
```
Replace 'your_password' with something secure and keep a record of it!

### 5. Add the Database Settings to the Memory Map Toolkit

Once you've configured the database, you then need to edit the Memory Map Toolkit configuration files.

The commands below create a new 'secret_settings.py' file (based on a template) and opens the Nano text editor.

```bash
cp memorymap_toolkit/settings/secret_settings_template.py memorymap_toolkit/settings/secret_settings.py
nano memorymap_toolkit/settings/secret_settings.py
```

You will see the following:

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'localhost',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
}

# If you want to use Google Analytics to monitor traffic to your site, put your tracking code here

GOOGLE_ANALYTICS_PROPERTY_ID = ''

# Uncomment the lines below if you've enabled SSL for your site. Not strictly secret settings, but kept here so they are kept out of version control.

# SECURE_SSL_HOST = True

# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE = True
```

Go to https://miniwebtool.com/django-secret-key-generator/ and generate a new secret key. Copy and paste this into the ```SECRET_KEY``` setting.

In ```ALLOWED_HOSTS``` add the domain name from which visitors will be able to view your map. For example, if people will go to www.mymemorymap.com, your allowed hosts setting will look like this:

```python
ALLOWED_HOSTS = ['www.mymemorymap.com']
```

In the ```DATABASES``` section, edit the ```NAME```, ```USER``` and ```PASSWORD```
settings to reflect how you configured the database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'localhost',
        'NAME': 'memorymap',
        'USER': 'memorymappper',
        'PASSWORD': 'your_password'
    }
}
```

Type ctrl+x to exit Nano, remembering to choose 'Yes' to save your changes.

When you've quit nano, run the following commands to migrate the database and copy the static files into the correct directory for deployment.

```bash
python manage.py migrate --settings=memorymap_toolkit.settings.local
python manage.py collectstatic --settings=memorymap_toolkit.settings.local
```

Finally, you need to create a user on the Toolkit so you can log in to the admin site:

```bash
python manage.py create_superuser --settings=memorymap_toolkit.settings.local
```

### 6. Test Everything Works

First, we'll need to open a port on the firewall:

```bash
sudo ufw allow 8000
```
Then we use Django's built-in test web server to test the site:

```bash
python manage.py runserver 0:8000 --settings=memorymap_toolkit.settings.local
```

In your web browser, enter the IP address of your server, followed by /memorymapper-admin/. For example, ```192.168.0.4/memorymapper-admin/```.

If everything worked, you will see the login page.

Go back to your terminal window and close port 8000 again:

```bash
sudo ufw deny 8000
```

### 7. Configure Apache

We have provided an example Apache configuration file to get you started. This is not the only way you can configure your web server, and if you have particular requirements it may not be suitable for your needs. See https://docs.djangoproject.com/en/3.0/howto/deployment/ for more details.

First, edit the example configuration:

```bash
nano example-apache-configuration.conf
```

Change the ```ServerName``` line to reflect the address from which users will access your Memory Map, eg: ```ServerName www.mymemorymap.com```. In the rest of the file, replace ```<your_user_name>``` with the name of the user account which you use to administer your server. For example, if you're logged in as memorymapper, the ```WSGIScriptAlias``` line will look like this: 

```
WSGIScriptAlias / /home/memorymapper/memorymap-toolkit
```

Once you've finished editing the configuration, quit Nano and save the file, and then copy it to your Apache configuration, naming it after the name of your website, eg:

```bash
sudo cp example-apache-configuration.conf /etc/apache2/sites-available/www.mymemorymap.com.conf
```

Then enable the configuration and restart Apache:
```bash
sudo a2dissite 000-default.conf
sudo a2ensite www.memorymap.com.conf
sudo apachectl restart --graceful
```

### 8. Connect Your Domain Name

It's beyond the scope of this document to give full instructions for configuring your domain name as the exact process varies according to your DNS provider. However, you need to add a new A record pointing to the IP address of your server so that it can be accessed over the web. Instructions for GoDaddy can be found here: https://uk.godaddy.com/help/manage-dns-zone-files-680

Once you've connected your domain name, you should now be able to visit your website at the correct address. However, when you first visit nothing will appear as some final configuration steps need to be completed.


### 9. Configure The Map

Visit ```www.mymemorymap.com/memorymapper-admin/``` and log in using the credentials you created using the ```create_superuser``` command you ran earlier.

Once you've logged in, click on the 'config' link (under 'Constance'). Most of these settings (at least initially) can be left at their defaults. However, there are couple of settings that need to be filled in before you can start using your map.

The Memory Map Toolbox ships with a basic map style which uses Ordnance Survey Open ZoomStack tiles hosted with MapTiler Cloud. This is a detailed base map covering the United Kingdom. In order to use it, you need to sign up for a free account with MapTiler Cloud (https://www.maptiler.com/cloud/) and copy your access key into the MAPTILER_KEY box.

The default map is a good base map choice if you're in the UK. However, if your memory map is located elsewhere, you'll need to use something else. The easiest option is to use a pre-created style from MapBox or MapTiler and copy the StyleJSON link (https://docs.mapbox.com/api/maps/#retrieve-a-style), including your access key, into the BASE_MAP_STYLE_URL box. If you're using a MapBox style, you also need to copy your key into the MAPBOX_KEY box.

Finally, you need to edit the MAP_CENTRE_LATITUDE and MAP_CENTER_LONGITUDE settings to change where your map is centred when it first loads.

Click the 'Save' button at the bottom of the page, and then click on the 'Visit Site' link in the top right hand corner.

All being well, you'll see a blank Memory Map, ready for you to get started.


### 10. Extra - SSL

We **highly recommend** that you install an SSL certificate so that traffic to and from your website is encrypted. This will also allow users on mobile platforms to share their location with your memory map and see where they are on the map.

The easiest (and cheapest) way to do this is to use LetsEncrypt and CertBot: follow the instructions at https://certbot.eff.org/lets-encrypt/ubuntufocal-apache to get started.


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

