# Generated by Django 3.2.18 on 2024-01-24 16:46

from django.db import migrations, models
import mmt_pages.models


class Migration(migrations.Migration):

    dependencies = [
        ('mmt_pages', '0005_auto_20231010_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to=mmt_pages.models.page_directory_path, verbose_name='Banner Image'),
        ),
    ]
