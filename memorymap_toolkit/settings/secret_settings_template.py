import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost')]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get('DJANGO_DB_HOST', 'localhost'),
        'NAME': os.environ.get('DJANGO_DB_NAME', ''),
        'USER': os.environ.get('DJANGO_DB_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', ''),
        'PORT': 5432
    }
}

# If you want to use Google Analytics to monitor traffic to your site, put your tracking code here

GOOGLE_ANALYTICS_PROPERTY_ID = ''

# Uncomment the lines below if you've enabled SSL for your site. Not strictly secret settings, but kept here so they are kept out of version control.

# SECURE_SSL_HOST = True

# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE = True