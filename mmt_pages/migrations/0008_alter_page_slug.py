# Generated by Django 3.2.18 on 2024-01-31 19:05

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mmt_pages', '0007_page_is_instructions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title'),
        ),
    ]
