# Generated by Django 5.0.4 on 2024-05-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_customuser_firebase_profile_picture_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_author',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='is user author'),
        ),
    ]
