# Generated by Django 5.0.4 on 2024-05-17 11:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0013_remove_song_albums_remove_playlistsongs_playlist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='publication_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 17, 11, 8, 51, 906945, tzinfo=datetime.timezone.utc), null=True, verbose_name='publication date'),
        ),
    ]
