# Generated by Django 3.2.18 on 2023-09-27 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mmt_pages', '0003_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Sections', to='mmt_pages.page'),
        ),
    ]
