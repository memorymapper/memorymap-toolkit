# Generated by Django 3.2.18 on 2023-08-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmt_pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_front_page',
            field=models.BooleanField(default=False),
        ),
    ]
