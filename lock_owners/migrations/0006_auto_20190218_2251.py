# Generated by Django 2.1.7 on 2019-02-18 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lock_owners', '0005_userimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='image_datetime',
            field=models.DateTimeField(help_text='Date and time the image was captured'),
        ),
    ]
