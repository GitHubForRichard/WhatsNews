# Generated by Django 3.0.6 on 2020-06-21 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notepad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='description',
            field=models.CharField(default='default', max_length=360),
            preserve_default=False,
        ),
    ]
