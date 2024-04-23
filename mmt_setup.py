import os
from mmt_pages.models import Page
from mmt_map.models import Theme
from django.contrib.auth.models import User


# Set up welcome and instructions pages, if needed

welcome_text = open('welcome.htm').read()
instructions_text = open('instructions.htm').read()

try:
    Page.objects.get(is_front_page=True)
except:
    Page.objects.create(title='Welcome', body=welcome_text, is_front_page=True).save()

try:
    Page.objects.get(is_instructions=True)
except:
    Page.objects.create(title='Instructions', body=instructions_text, is_instructions=True).save()


# Create a default theme, if needed
    
if Theme.objects.all().count() == 0:
    t = Theme.objects.create(name='Default')
    t.save()


# Create a superuser, if needs be

try:
    User.objects.filter(is_superuser=True)[0]
except:
    pw = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    if pw:
        u = User.objects.create(username=os.environ.get('DJANGO_SUPERUSER', 'admin'), is_superuser=True, is_staff=True)
        u.set_password(pw)
        u.save()