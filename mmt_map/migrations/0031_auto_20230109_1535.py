# Generated by Django 3.1.13 on 2023-01-09 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmt_map', '0030_auto_20221215_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='thumbnail_url',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='point',
            name='thumbnail_url',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='polygon',
            name='thumbnail_url',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]