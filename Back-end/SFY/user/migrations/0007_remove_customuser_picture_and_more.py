# Generated by Django 5.0.4 on 2024-05-14 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_customuser_firebase_profile_picture_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='picture',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='firebase_profile_picture_url',
            field=models.CharField(blank=True, default='sfy-firebase.appspot.com/profile_pictures/defaultuser.png', max_length=500, null=True),
        ),
    ]
