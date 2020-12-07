import os
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY") 

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS")]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get("DB_HOST"),
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USERNAME"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'OPTIONS': {
            'sslmode':'prefer',
        }
    }

}

# If you want to use Google Analytics to monitor traffic to your site, put your tracking code here

GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get("ANALYTICS_ID")

# Uncomment the lines below if you've enabled SSL for your site. Not strictly secret settings, but kept here so they are kept out of version control.

# SECURE_SSL_HOST = True

# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE = True
