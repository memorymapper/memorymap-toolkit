# Generated by Django 3.2.18 on 2024-07-02 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmt_map', '0041_auto_20240612_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
