# Generated by Django 3.1.13 on 2022-12-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmt_map', '0029_taglist'),
    ]

    operations = [
        migrations.AddField(
            model_name='taglist',
            name='order',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='taglist',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
