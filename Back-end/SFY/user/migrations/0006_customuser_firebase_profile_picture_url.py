# Generated by Django 5.0.4 on 2024-05-14 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='firebase_profile_picture_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
