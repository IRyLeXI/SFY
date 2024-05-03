# Generated by Django 5.0.4 on 2024-05-03 13:24

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='followers',
            field=models.ManyToManyField(related_name='followed_playlists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='is_private',
            field=models.BooleanField(default=True, verbose_name='is private'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='created_date',
            field=models.DateField(default=datetime.date(2024, 5, 3), editable=False, verbose_name='created date'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='updated_date',
            field=models.DateField(default=datetime.date(2024, 5, 3), verbose_name='updated date'),
        ),
    ]
