# Generated by Django 5.0.4 on 2024-05-16 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0011_alter_song_publication_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='publication_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 16, 13, 59, 44, 260485, tzinfo=datetime.timezone.utc), null=True, verbose_name='publication date'),
        ),
    ]
