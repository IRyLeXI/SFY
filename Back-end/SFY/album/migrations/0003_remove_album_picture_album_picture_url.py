# Generated by Django 5.0.4 on 2024-05-14 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0002_alter_album_created_date_alter_album_publish_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='picture',
        ),
        migrations.AddField(
            model_name='album',
            name='picture_url',
            field=models.CharField(blank=True, default='sfy-firebase.appspot.com/albums_pictures/defaultalbum.png', max_length=255, null=True, verbose_name='album picture'),
        ),
    ]
