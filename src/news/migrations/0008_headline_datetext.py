# Generated by Django 3.0.6 on 2020-05-26 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_headline_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='headline',
            name='dateText',
            field=models.CharField(default='', max_length=120),
        ),
    ]
