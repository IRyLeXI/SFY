# Generated by Django 5.0.4 on 2024-05-15 14:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0007_remove_playlist_picture_playlist_picture_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='created_date',
            field=models.DateField(default=datetime.date(2024, 5, 15), editable=False, verbose_name='created date'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='updated_date',
            field=models.DateField(default=datetime.date(2024, 5, 15), verbose_name='updated date'),
        ),
    ]
